"""Настройки сервиса: читаются из переменных окружения."""
import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = APP_DIR / "web"
MIGRATIONS_DIR = APP_DIR / "migrations"
TASKS_DIR = APP_DIR / "data" / "tasks"

DEFAULT_APP_URL = "postgresql://guide:guide@127.0.0.1:5432/learning_shop"
DEFAULT_LEARNER_URL = "postgresql://learner_ro:learner_ro_dev@127.0.0.1:5432/learning_shop"


class Settings:
    database_url: str = os.getenv("DATABASE_URL", DEFAULT_APP_URL)
    learner_database_url: str = os.getenv("LEARNER_DATABASE_URL", DEFAULT_LEARNER_URL)
    learner_password: str = os.getenv("LEARNER_PASSWORD", "learner_ro_dev")
    cookie_secure: bool = os.getenv("COOKIE_SECURE", "0") == "1"
    session_days: int = int(os.getenv("SESSION_DAYS", "30"))
    allowed_origin: str = os.getenv("ALLOWED_ORIGIN", "")
    statement_timeout_ms: int = int(os.getenv("STATEMENT_TIMEOUT_MS", "3000"))
    max_rows: int = int(os.getenv("MAX_ROWS", "100"))
    default_pandas_url: str = os.getenv("BOOK_URL", "https://aleksey-s-lozhkin.github.io/python-sql-guide/")


settings = Settings()
