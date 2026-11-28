-- Справочник «Дата и время»: SQL. Все примеры страницы ref-dt-sql.html.
--
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_dt_sql_lab.sql
--
-- PostgreSQL 14, база learning_shop.
-- Только SELECT и EXPLAIN: база не меняется.
-- В начале фиксируются зона сессии и DateStyle, чтобы вывод не зависел
-- от настроек машины. Даты в примерах заданы литералами — now() нет,
-- поэтому вывод воспроизводим.
--
-- Нужны базовая схема learning_shop и таблица orders_big (100 000 строк):
--     bash tools/setup_db.sh
--     psql -d learning_shop -f guide/snippets/ref_sql_setup.sql

\set ON_ERROR_STOP on
SET TIME ZONE 'UTC';
SET DateStyle = 'ISO, MDY';

\echo '== 03 Синтаксис-шаблон: четыре литерала =='
SELECT DATE '2024-01-01' AS d,
       TIMESTAMP '2024-01-01 12:30:00' AS naive,
       TIMESTAMPTZ '2024-01-01 12:30:00+03' AS moment,
       INTERVAL '1 day 2 hours' AS span;

\echo '== 05.1 Четыре типа и pg_typeof =='
SELECT pg_typeof(DATE '2024-01-01') AS d,
       pg_typeof(TIMESTAMP '2024-01-01 12:30:00') AS naive,
       pg_typeof(TIMESTAMPTZ '2024-01-01 12:30:00+03') AS moment,
       pg_typeof(INTERVAL '1 day') AS span;

\echo '== 05.2 date_trunc, extract и to_char =='
SELECT id,
       created_at,
       date_trunc('month', created_at) AS month_start,
       extract(year FROM created_at) AS yr,
       to_char(created_at, 'YYYY-MM-DD') AS day
FROM orders
WHERE id <= 3
ORDER BY id;

\echo '== 05.3 Арифметика: interval и разность timestamp =='
SELECT id,
       created_at + INTERVAL '1 day' AS next_day,
       created_at - TIMESTAMP '2024-01-01 00:00:00' AS since_start
FROM orders
WHERE id <= 3
ORDER BY id;

\echo '== 05.4 date - date, age и epoch =='
SELECT DATE '2024-03-20' - DATE '2024-01-05' AS days,
       age(TIMESTAMP '2024-03-20 15:55:00', TIMESTAMP '2024-01-01 00:00:00') AS gap,
       extract(epoch FROM TIMESTAMP '2024-01-01 00:00:00')::bigint AS epoch_s;

\echo '== 05.5 AT TIME ZONE и SET TIME ZONE =='
SET TIME ZONE 'Europe/Moscow';
SELECT TIMESTAMPTZ '2024-01-01 12:30:00+03' AS moment;

SET TIME ZONE 'UTC';
SELECT TIMESTAMPTZ '2024-01-01 12:30:00+03' AS moment;

SELECT TIMESTAMPTZ '2024-01-01 12:30:00+03' AT TIME ZONE 'Europe/Moscow' AS moscow_wall,
       TIMESTAMPTZ '2024-01-01 12:30:00+03' AT TIME ZONE 'UTC' AS utc_wall;

\echo '== 05.6 Границы периода: полуинтервал против BETWEEN =='
SELECT COUNT(*) AS half_open
FROM orders_big
WHERE created_at >= TIMESTAMP '2024-02-01'
  AND created_at <  TIMESTAMP '2024-02-02';

SELECT COUNT(*) AS between_closed
FROM orders_big
WHERE created_at BETWEEN TIMESTAMP '2024-02-01' AND TIMESTAMP '2024-02-02';

\echo '== 05.7 Индекс: диапазон по колонке и ::date =='
EXPLAIN (COSTS OFF) SELECT * FROM orders_big
WHERE created_at >= TIMESTAMP '2024-03-09';

EXPLAIN (COSTS OFF) SELECT * FROM orders_big
WHERE created_at::date = DATE '2024-03-09';

\echo '== 06.1 Сценарий: месячная выручка =='
SELECT date_trunc('month', o.created_at)::date AS month,
       COUNT(*) AS orders,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY 1
ORDER BY 1;

\echo '== 06.2 Сценарий: последние N дней =='
SELECT id, created_at
FROM orders
WHERE created_at >= TIMESTAMP '2024-02-15'
ORDER BY created_at DESC, id
LIMIT 5;

\echo '== 06.3 Сценарий: отчёт с TZ-конверсией =='
SELECT id,
       created_at AT TIME ZONE 'UTC' AS as_utc,
       created_at AT TIME ZONE 'Europe/Moscow' AS as_moscow
FROM orders
WHERE id <= 3
ORDER BY id;

\echo '== 08a Задача: выручка по месяцам и городам =='
SELECT COALESCE(NULLIF(TRIM(u.city), ''), 'не указан') AS city,
       date_trunc('month', o.created_at)::date AS month,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY 1, date_trunc('month', o.created_at)
ORDER BY month, city;

\echo '== 08b Задача: epoch первого заказа месяца =='
SELECT date_trunc('month', created_at)::date AS month,
       MIN(extract(epoch FROM created_at))::bigint AS first_epoch_s
FROM orders
GROUP BY 1
ORDER BY 1;
