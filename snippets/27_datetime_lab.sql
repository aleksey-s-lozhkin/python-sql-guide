-- Спецглава 27: дата и время. Лаборатория.
-- База: learning_shop (PostgreSQL 14). Только SELECT.
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/27_datetime_lab.sql
--
-- Сессия переводится в UTC, чтобы EXTRACT(EPOCH ...) и вывод timestamptz
-- не зависели от локальной зоны машины. Все даты фиксированные:
-- now() и current_timestamp не используются.

SET TIME ZONE 'UTC';

\echo '── 06.1. Типы даты и времени ──'
SELECT DATE '2024-03-15' AS d,
       TIMESTAMP '2024-03-15 12:30:00' AS ts,
       INTERVAL '2 hours 15 minutes' AS dur;

\echo '── 06.2. timestamp и timestamptz ──'
SHOW TIME ZONE;

SELECT TIMESTAMP '2024-03-15 12:30:00' AS wall_clock,
       TIMESTAMPTZ '2024-03-15 12:30:00+03' AS same_instant;

\echo '── 06.3. Epoch ──'
SELECT EXTRACT(EPOCH FROM TIMESTAMP '2024-03-15 12:30:00') AS epoch_ts,
       EXTRACT(EPOCH FROM TIMESTAMPTZ '2024-03-15 12:30:00+00') AS epoch_tstz;

\echo '── 06.4. Календарная арифметика ──'
SELECT TIMESTAMP '2024-01-31 00:00:00' + INTERVAL '1 month' AS plus_month,
       TIMESTAMP '2024-03-15 12:30:00' - TIMESTAMP '2024-03-01 00:00:00' AS diff;

\echo '── 06.5. date_trunc, EXTRACT и to_char ──'
SELECT o.id,
       DATE_TRUNC('month', o.created_at)::date AS month,
       EXTRACT(DAY FROM o.created_at) AS day,
       TO_CHAR(o.created_at, 'DD.MM.YYYY HH24:MI') AS pretty
FROM orders o
ORDER BY o.id
LIMIT 3;

\echo '── 06.6. BETWEEN и полуоткрытый интервал ──'
SELECT COUNT(*) AS between_rows
FROM orders
WHERE created_at BETWEEN TIMESTAMP '2024-01-05' AND TIMESTAMP '2024-01-05';

SELECT COUNT(*) AS range_rows
FROM orders
WHERE created_at >= TIMESTAMP '2024-01-05'
  AND created_at <  TIMESTAMP '2024-01-06';

\echo '── 07.1. Выручка по месяцам ──'
SELECT DATE_TRUNC('month', o.created_at)::date AS month,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY 1
ORDER BY 1;

\echo '── 07.2. AT TIME ZONE ──'
SELECT TIMESTAMPTZ '2024-03-15 12:30:00+00' AT TIME ZONE 'Europe/Moscow' AS moscow,
       TIMESTAMPTZ '2024-03-15 12:30:00+00' AT TIME ZONE 'Asia/Tokyo' AS tokyo;

\echo '── 10.1. Задача: топ-3 дня по выручке ──'
SELECT o.created_at::date AS day,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY 1
ORDER BY revenue DESC, day
LIMIT 3;
