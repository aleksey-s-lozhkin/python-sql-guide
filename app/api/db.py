"""Подключение к PostgreSQL и подготовка схемы `app`."""
from contextlib import contextmanager

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

from .settings import MIGRATIONS_DIR, settings


@contextmanager
def connect(url=None):
    conn = psycopg.connect(url or settings.database_url, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def ensure_schema():
    """Создаёт app-схему, роль только для чтения и выдаёт ей SELECT на public."""
    with connect() as conn:
        with conn.cursor() as cur:
            migration = (MIGRATIONS_DIR / "001_app.sql").read_text(encoding="utf-8")
            cur.execute(migration)
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'learner_ro'")
            if cur.fetchone() is None:
                cur.execute(
                    sql.SQL("CREATE ROLE learner_ro LOGIN PASSWORD {}").format(
                        sql.Literal(settings.learner_password)
                    )
                )
            else:
                cur.execute(
                    sql.SQL("ALTER ROLE learner_ro WITH LOGIN PASSWORD {}").format(
                        sql.Literal(settings.learner_password)
                    )
                )
            cur.execute("GRANT USAGE ON SCHEMA public TO learner_ro")
            cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO learner_ro")
        conn.commit()


def healthcheck():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            return cur.fetchone()["ok"] == 1
