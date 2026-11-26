-- Схема сервиса: пользователи, сессии, прогресс и попытки.
-- Выполняется при старте приложения (idempotent).

CREATE SCHEMA IF NOT EXISTS app;

CREATE TABLE IF NOT EXISTS app.users (
    id            BIGSERIAL PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS app.sessions (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS sessions_user_idx ON app.sessions (user_id);

CREATE TABLE IF NOT EXISTS app.progress (
    user_id      BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    chapter_slug TEXT NOT NULL,
    status       TEXT NOT NULL CHECK (status IN ('started', 'done')),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, chapter_slug)
);

CREATE TABLE IF NOT EXISTS app.submissions (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
    task_slug   TEXT NOT NULL,
    sql_text    TEXT NOT NULL,
    ok          BOOLEAN NOT NULL,
    error       TEXT,
    duration_ms INTEGER,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS submissions_user_idx ON app.submissions (user_id, created_at DESC);
