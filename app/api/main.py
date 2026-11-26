"""FastAPI-сервис практики: аккаунты, прогресс и проверка SQL-задач."""
import re
import time

import psycopg
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import checker, tasks
from .db import connect, ensure_schema, healthcheck
from .security import (
    COOKIE_NAME,
    create_session,
    delete_session,
    get_user,
    hash_password,
    verify_password,
)
from .settings import WEB_DIR, settings
from .sql_runner import SqlError, execute_readonly, execute_reference, validate_sql

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


class AuthBody(BaseModel):
    email: str
    password: str


class ProgressBody(BaseModel):
    status: str


class CheckBody(BaseModel):
    sql: str


app = FastAPI(title="Guide Practice", docs_url=None, redoc_url=None)


@app.on_event("startup")
def startup() -> None:
    ensure_schema()
    tasks.load_tasks()


@app.middleware("http")
async def origin_guard(request: Request, call_next):
    if settings.allowed_origin and request.method in ("POST", "PUT", "DELETE"):
        origin = request.headers.get("origin")
        if origin and origin.rstrip("/") != settings.allowed_origin.rstrip("/"):
            return JSONResponse({"detail": "Запрос с другого источника запрещён."}, status_code=403)
    return await call_next(request)


def require_user(request: Request):
    user = get_user(request.cookies.get(COOKIE_NAME, ""))
    if not user:
        raise HTTPException(status_code=401, detail="Нужно войти.")
    return user


def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=settings.session_days * 24 * 3600,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )


@app.get("/health")
def health():
    try:
        return {"ok": True, "db": healthcheck(), "tasks": len(tasks.all_tasks())}
    except psycopg.Error:
        return JSONResponse({"ok": False, "db": False}, status_code=503)


@app.get("/api/config")
def config():
    return {"book_url": settings.default_pandas_url}


@app.post("/api/auth/register")
def register(body: AuthBody, response: Response):
    email = body.email.strip().lower()
    if not EMAIL_RE.match(email):
        raise HTTPException(status_code=400, detail="Некорректный email.")
    if len(body.password) < 8:
        raise HTTPException(status_code=400, detail="Пароль должен быть не короче 8 символов.")
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO app.users (email, password_hash) VALUES (%s, %s) RETURNING id",
                    (email, hash_password(body.password)),
                )
                user_id = cur.fetchone()["id"]
            conn.commit()
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже есть.")
    token = create_session(user_id)
    set_session_cookie(response, token)
    return {"email": email}


@app.post("/api/auth/login")
def login(body: AuthBody, response: Response):
    email = body.email.strip().lower()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, password_hash FROM app.users WHERE email = %s", (email,))
            row = cur.fetchone()
    if not row or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Неверный email или пароль.")
    token = create_session(row["id"])
    set_session_cookie(response, token)
    return {"email": email}


@app.post("/api/auth/logout")
def logout(request: Request, response: Response):
    delete_session(request.cookies.get(COOKIE_NAME, ""))
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"ok": True}


@app.get("/api/me")
def me(request: Request):
    user = require_user(request)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) AS n FROM app.progress WHERE user_id = %s", (user["id"],))
            count = cur.fetchone()["n"]
    return {"email": user["email"], "progress_count": count}


@app.get("/api/progress")
def get_progress(request: Request):
    user = require_user(request)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT chapter_slug, status, updated_at FROM app.progress WHERE user_id = %s",
                (user["id"],),
            )
            rows = cur.fetchall()
    return {
        "items": [
            {"slug": r["chapter_slug"], "status": r["status"], "updated_at": r["updated_at"].isoformat()}
            for r in rows
        ]
    }


@app.put("/api/progress/{slug}")
def put_progress(slug: str, body: ProgressBody, request: Request):
    user = require_user(request)
    if not SLUG_RE.match(slug):
        raise HTTPException(status_code=400, detail="Некорректный slug главы.")
    if body.status not in ("started", "done"):
        raise HTTPException(status_code=400, detail="status: started или done.")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO app.progress (user_id, chapter_slug, status)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, chapter_slug)
                DO UPDATE SET status = EXCLUDED.status, updated_at = now()
                """,
                (user["id"], slug, body.status),
            )
        conn.commit()
    return {"ok": True}


@app.delete("/api/progress/{slug}")
def delete_progress(slug: str, request: Request):
    user = require_user(request)
    if not SLUG_RE.match(slug):
        raise HTTPException(status_code=400, detail="Некорректный slug главы.")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM app.progress WHERE user_id = %s AND chapter_slug = %s",
                (user["id"], slug),
            )
        conn.commit()
    return {"ok": True}


@app.get("/api/tasks")
def list_tasks():
    return {"items": [tasks.task_list(t) for t in tasks.all_tasks()]}


@app.get("/api/tasks/{slug}")
def task_detail(slug: str):
    task = tasks.get_task(slug)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")
    return tasks.public_task(task)


@app.post("/api/tasks/{slug}/check")
def check_task(slug: str, body: CheckBody, request: Request):
    user = require_user(request)
    task = tasks.get_task(slug)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT count(*) AS n FROM app.submissions "
                "WHERE user_id = %s AND created_at > now() - interval '2 seconds'",
                (user["id"],),
            )
            if cur.fetchone()["n"]:
                raise HTTPException(status_code=429, detail="Подождите пару секунд перед следующей попыткой.")

    started = time.perf_counter()
    try:
        validate_sql(body.sql)
        got_columns, got_rows = execute_readonly(body.sql)
        ref_columns, ref_rows = execute_reference(task.reference)
    except SqlError as exc:
        _record(user["id"], task.slug, body.sql, False, str(exc), started)
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=200)

    result = checker.compare(got_rows, ref_rows, ordered=task.ordered)
    if result.get("ok") and len(got_columns) != len(ref_columns):
        result = {
            "ok": False,
            "error": "Ожидалось колонок: {}, получено: {}.".format(len(ref_columns), len(got_columns)),
            "expected_count": len(ref_rows),
            "got_count": len(got_rows),
        }
    result["columns"] = got_columns
    result["rows"] = [
        [checker.normalize_value(v) for v in row] for row in got_rows[:20]
    ]
    result["preview_limit"] = 20
    _record(user["id"], task.slug, body.sql, bool(result["ok"]), result.get("error"), started)
    return result


def _record(user_id: int, slug: str, sql: str, ok: bool, error, started: float) -> None:
    duration = int((time.perf_counter() - started) * 1000)
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO app.submissions (user_id, task_slug, sql_text, ok, error, duration_ms) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (user_id, slug, sql[:4000], ok, (error or "")[:1000], duration),
                )
            conn.commit()
    except psycopg.Error:
        pass


@app.get("/api/submissions")
def submissions(request: Request):
    user = require_user(request)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT task_slug, ok, error, duration_ms, created_at FROM app.submissions "
                "WHERE user_id = %s ORDER BY created_at DESC LIMIT 20",
                (user["id"],),
            )
            rows = cur.fetchall()
    return {
        "items": [
            {
                "task": r["task_slug"],
                "ok": r["ok"],
                "error": r["error"],
                "ms": r["duration_ms"],
                "at": r["created_at"].isoformat(),
            }
            for r in rows
        ]
    }


app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
