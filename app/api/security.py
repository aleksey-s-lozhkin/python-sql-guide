"""Пароли и сессии без внешних зависимостей (scrypt из стандартной библиотеки)."""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from .db import connect
from .settings import settings

COOKIE_NAME = "guide_session"
_PBKDF2_ITERATIONS = 300_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS, dklen=32)
    return "pbkdf2${}${}${}".format(_PBKDF2_ITERATIONS, salt.hex(), digest.hex())


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iterations, salt_hex, digest_hex = stored.split("$")
        if algo != "pbkdf2":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
            dklen=len(bytes.fromhex(digest_hex)),
        )
        return secrets.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(days=settings.session_days)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO app.sessions (user_id, token_hash, expires_at) VALUES (%s, %s, %s)",
                (user_id, _token_hash(token), expires),
            )
        conn.commit()
    return token


def get_user(token: str):
    if not token:
        return None
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.id, u.email, s.expires_at
                FROM app.sessions s
                JOIN app.users u ON u.id = s.user_id
                WHERE s.token_hash = %s AND s.expires_at > now()
                """,
                (_token_hash(token),),
            )
            return cur.fetchone()


def delete_session(token: str) -> None:
    if not token:
        return
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM app.sessions WHERE token_hash = %s", (_token_hash(token),))
        conn.commit()
