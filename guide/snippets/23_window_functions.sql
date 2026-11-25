-- Глава 23: оконные функции. База: learning_shop.

-- 1. ROW_NUMBER, RANK, DENSE_RANK при равных значениях
WITH t(name, score) AS (
    VALUES ('a', 100), ('b', 100), ('c', 90), ('d', 80)
)
SELECT name, score,
       ROW_NUMBER() OVER (ORDER BY score DESC) AS rn,
       RANK()       OVER (ORDER BY score DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense
FROM t;

-- 2. Рейтинг пользователей по выручке
SELECT u.name, SUM(o.quantity * p.price) AS revenue,
       ROW_NUMBER() OVER (ORDER BY SUM(o.quantity * p.price) DESC) AS place
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
ORDER BY revenue DESC;

-- 3. Накопительная сумма, LAG и доля
WITH order_revenue AS (
    SELECT o.id, o.user_id, o.created_at, o.quantity * p.price AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
)
SELECT u.name, r.created_at::date AS day, r.revenue,
       SUM(r.revenue) OVER (PARTITION BY r.user_id ORDER BY r.created_at) AS running,
       LAG(r.revenue) OVER (PARTITION BY r.user_id ORDER BY r.created_at) AS prev,
       ROUND(100.0 * r.revenue / SUM(r.revenue) OVER (PARTITION BY r.user_id), 1) AS pct
FROM order_revenue r
JOIN users u ON u.id = r.user_id
ORDER BY u.name, r.created_at;

-- 4. Первый заказ каждого пользователя (top-1 на группу)
WITH ranked AS (
    SELECT u.name, o.created_at::date AS day, o.quantity * p.price AS revenue,
           ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.created_at) AS rn
    FROM orders o
    JOIN users u ON u.id = o.user_id
    JOIN products p ON p.id = o.product_id
)
SELECT name, day, revenue
FROM ranked WHERE rn = 1
ORDER BY name;

-- 5. Итог рядом с каждой строкой
SELECT u.name, (o.quantity * p.price) AS revenue,
       SUM(o.quantity * p.price) OVER () AS total_all
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
WHERE u.name = 'Anna'
ORDER BY o.created_at;
