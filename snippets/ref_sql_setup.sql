-- Справочник SQL: подготовка базы learning_shop к лабораториям.
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_setup.sql
--
-- Что делает:
--   1) проверяет, что базовая схема создана (users / products / orders);
--   2) создаёт orders_big (100 000 строк), если её ещё нет;
--   3) добавляет индексы orders_big, если их нет;
--   4) фиксирует статистику (полная выборка), чтобы планы EXPLAIN на странице
--      «Индексы и EXPLAIN» были воспроизводимы, а не зависели от случайной
--      выборки ANALYZE.
--
-- Идемпотентен: повторный запуск ничего не меняет и не ломает.
-- Страницам 01–05 достаточно базовой схемы; orders_big нужна только странице 06.

\set ON_ERROR_STOP on

-- 1. База должна быть создана заранее: bash tools/setup_db.sh
DO $$
BEGIN
    IF to_regclass('public.users') IS NULL
       OR to_regclass('public.products') IS NULL
       OR to_regclass('public.orders') IS NULL THEN
        RAISE EXCEPTION 'Нет таблиц users/products/orders. Сначала выполните: bash tools/setup_db.sh';
    END IF;
END $$;

-- 2. orders_big: та же схема и данные, что в главе 24.
DO $$
BEGIN
    IF to_regclass('public.orders_big') IS NULL THEN
        CREATE TABLE orders_big AS
        SELECT gs AS id,
               (gs % 5) + 1 AS user_id,
               (gs % 6) + 1 AS product_id,
               (gs % 3) + 1 AS quantity,
               timestamp '2024-01-01' + (gs || ' minutes')::interval AS created_at
        FROM generate_series(1, 100000) AS gs;
        RAISE NOTICE 'orders_big: создана (100000 строк)';
    ELSE
        RAISE NOTICE 'orders_big: уже есть, пропускаю создание';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = to_regclass('public.orders_big')
          AND contype = 'p'
    ) THEN
        ALTER TABLE orders_big ADD PRIMARY KEY (id);
    END IF;
END $$;

-- 3. Индексы, на которых построены примеры страницы 06.
CREATE INDEX IF NOT EXISTS idx_orders_big_user ON orders_big (user_id);
CREATE INDEX IF NOT EXISTS idx_orders_big_created ON orders_big (created_at);

-- 4. Полная статистика: 10000 * 300 > 100000, поэтому ANALYZE читает все строки,
--    и оценки rows/cost перестают «плавать» между запусками.
ALTER TABLE orders_big ALTER COLUMN id SET STATISTICS 10000;
ALTER TABLE orders_big ALTER COLUMN user_id SET STATISTICS 10000;
ALTER TABLE orders_big ALTER COLUMN product_id SET STATISTICS 10000;
ALTER TABLE orders_big ALTER COLUMN quantity SET STATISTICS 10000;
ALTER TABLE orders_big ALTER COLUMN created_at SET STATISTICS 10000;

ANALYZE users;
ANALYZE products;
ANALYZE orders;
ANALYZE orders_big;

\echo 'Готово: learning_shop подготовлена к SQL-лабораториям.'
