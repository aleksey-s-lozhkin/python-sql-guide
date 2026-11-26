"""Безопасное выполнение пользовательского SELECT.

Правила:
  * один запрос, начинающийся с SELECT или WITH;
  * запрещены DML/DDL, транзакции, COPY, вызовы pg_*, несколько выражений;
  * соединение идёт под ролью learner_ro (только SELECT на public), в read-only транзакции;
  * statement_timeout и лимит строк защищают от тяжёлых запросов.
"""
import re

import psycopg
import sqlparse
from psycopg import sql as pgsql
from sqlparse import tokens as T

from .settings import settings

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|do|call|"
    r"vacuum|analyze|reindex|cluster|listen|notify|unlisten|set|reset|show|explain|lock|"
    r"begin|commit|rollback|savepoint|release|prepare|execute|deallocate|discard|merge|into)\b",
    re.IGNORECASE,
)
FORBIDDEN_FUNCS = re.compile(r"\bpg_\w+", re.IGNORECASE)


class SqlError(Exception):
    """Ошибка проверки или выполнения SQL — показывается ученику."""


def _strip_literals(raw: str) -> str:
    parts = []
    for statement in sqlparse.parse(raw):
        for token in statement.flatten():
            if token.ttype in T.Literal.String or token.ttype in T.Comment:
                parts.append(" ")
            else:
                parts.append(token.value)
    return "".join(parts)


def validate_sql(raw: str) -> str:
    sql = (raw or "").strip()
    if not sql:
        raise SqlError("Пустой запрос.")
    statements = [s for s in sqlparse.split(sql) if s.strip()]
    if len(statements) != 1:
        raise SqlError("Разрешён только один SQL-запрос.")
    parsed = sqlparse.parse(sql)
    first = parsed[0].token_first(skip_ws=True, skip_cm=True)
    keyword = (first.value if first else "").upper()
    if keyword not in ("SELECT", "WITH"):
        raise SqlError("Запрос должен начинаться с SELECT или WITH.")
    bare = _strip_literals(sql)
    match = FORBIDDEN.search(bare)
    if match:
        raise SqlError("В запросе запрещено слово «{}»: разрешены только SELECT-запросы.".format(match.group(0)))
    func = FORBIDDEN_FUNCS.search(bare)
    if func:
        raise SqlError("Системные функции {} запрещены.".format(func.group(0)))
    return sql


def _wrap(sql: str) -> str:
    return "SELECT * FROM (\n{}\n) AS guide_query LIMIT {}".format(
        sql.rstrip().rstrip(";"), settings.max_rows + 1
    )


def execute_readonly(sql: str):
    """Выполняет проверенный SQL под ролью только для чтения. Возвращает (columns, rows)."""
    wrapped = _wrap(sql)
    try:
        with psycopg.connect(settings.learner_database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(pgsql.SQL("SET LOCAL statement_timeout = {}").format(pgsql.Literal("{}ms".format(settings.statement_timeout_ms))))
                cur.execute("SET LOCAL default_transaction_read_only = on")
                cur.execute("SET LOCAL search_path TO public")
                cur.execute(wrapped)
                columns = [d.name for d in cur.description] if cur.description else []
                rows = cur.fetchall()
            conn.rollback()
    except psycopg.errors.UndefinedColumn as exc:
        raise SqlError("Нет такой колонки: {}".format(exc.diag.message_primary or exc)) from exc
    except psycopg.errors.UndefinedTable as exc:
        raise SqlError("Нет такой таблицы: {}".format(exc.diag.message_primary or exc)) from exc
    except psycopg.errors.SyntaxError as exc:
        raise SqlError("Синтаксическая ошибка: {}".format(exc.diag.message_primary or exc)) from exc
    except psycopg.errors.QueryCanceled as exc:
        raise SqlError("Запрос выполнялся слишком долго и был остановлен.") from exc
    except psycopg.Error as exc:
        raise SqlError("Ошибка базы: {}".format(exc.diag.message_primary or exc)) from exc

    if len(rows) > settings.max_rows:
        raise SqlError(
            "Слишком много строк: сузьте выборку (LIMIT или более точный фильтр)."
        )
    return columns, rows


def execute_reference(sql: str):
    """Выполняет эталонный запрос (доверенный) в той же read-only манере."""
    wrapped = _wrap(sql)
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(pgsql.SQL("SET LOCAL statement_timeout = {}").format(pgsql.Literal("{}ms".format(settings.statement_timeout_ms))))
            cur.execute("SET LOCAL default_transaction_read_only = on")
            cur.execute("SET LOCAL search_path TO public")
            cur.execute(wrapped)
            columns = [d.name for d in cur.description] if cur.description else []
            rows = cur.fetchall()
        conn.rollback()
    return columns, rows
