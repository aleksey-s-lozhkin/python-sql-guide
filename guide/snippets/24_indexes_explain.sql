-- Глава 24: индексы и EXPLAIN. База: learning_shop.
-- Таблица побольше, чтобы планировщик мог выбрать индекс.

DROP TABLE IF EXISTS orders_big;
CREATE TABLE orders_big AS
SELECT gs AS id,
       (gs % 5) + 1 AS user_id,
       (gs % 6) + 1 AS product_id,
       (gs % 3) + 1 AS quantity,
       timestamp '2024-01-01' + (gs || ' minutes')::interval AS created_at
FROM generate_series(1, 100000) AS gs;
ALTER TABLE orders_big ADD PRIMARY KEY (id);
ANALYZE orders_big;

-- 1. Без индекса: Seq Scan
EXPLAIN ANALYZE SELECT * FROM orders_big WHERE user_id = 3;

-- 2. Индекс по user_id: Bitmap Heap Scan
CREATE INDEX idx_orders_big_user ON orders_big(user_id);
ANALYZE orders_big;
EXPLAIN ANALYZE SELECT * FROM orders_big WHERE user_id = 3;

-- 3. Узкий диапазон по created_at: Index Scan
CREATE INDEX idx_orders_big_created ON orders_big(created_at);
ANALYZE orders_big;
EXPLAIN ANALYZE SELECT * FROM orders_big
WHERE created_at >= '2024-01-02' AND created_at < '2024-01-03';

-- 4. Функция на колонке: Seq Scan, индекс не используется
EXPLAIN ANALYZE SELECT * FROM orders_big
WHERE EXTRACT(MONTH FROM created_at) = 3;

-- 5. План соединения на маленькой базе
EXPLAIN SELECT o.id, u.name, p.name
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
WHERE u.city = 'Москва';
