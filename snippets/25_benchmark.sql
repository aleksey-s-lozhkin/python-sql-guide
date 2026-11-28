-- Глава 25: замер SQL против pandas. База: learning_shop, таблица orders_big.
-- Сначала создайте orders_big (см. 24_indexes_explain.sql).

\timing on
SELECT user_id, SUM(quantity * price) AS revenue
FROM orders_big o
JOIN products p ON p.id = o.product_id
GROUP BY user_id
ORDER BY user_id;
