-- Глава 26: проект — отчёт из нескольких таблиц. База: learning_shop.

-- 1. Выручка, заказы и средний чек по месяцам
WITH order_revenue AS (
    SELECT o.id, o.created_at, o.quantity * p.price AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
)
SELECT DATE_TRUNC('month', created_at)::date AS month,
       COUNT(*) AS orders,
       SUM(revenue) AS revenue,
       ROUND(AVG(revenue), 2) AS avg_check
FROM order_revenue
GROUP BY 1 ORDER BY 1;

-- 2. Топ-3 пользователей
SELECT u.name, SUM(o.quantity * p.price) AS revenue,
       COUNT(*) AS orders,
       RANK() OVER (ORDER BY SUM(o.quantity * p.price) DESC) AS place
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
ORDER BY revenue DESC
LIMIT 3;

-- 3. Доля категорий
WITH category_revenue AS (
    SELECT p.category, SUM(o.quantity * p.price) AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
    GROUP BY p.category
)
SELECT category, revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS share_pct
FROM category_revenue
ORDER BY revenue DESC;

-- 4. Гостевые заказы
SELECT COUNT(*) AS guest_orders,
       SUM(o.quantity * p.price) AS guest_revenue,
       ROUND(100.0 * SUM(o.quantity * p.price) /
             (SELECT SUM(o2.quantity * p2.price)
              FROM orders o2 JOIN products p2 ON p2.id = o2.product_id), 2) AS share_pct
FROM orders o
JOIN products p ON p.id = o.product_id
WHERE NOT EXISTS (SELECT 1 FROM users u WHERE u.id = o.user_id);

-- 5. Контроль: общая выручка
SELECT SUM(quantity * price) AS total_revenue
FROM orders o JOIN products p ON p.id = o.product_id;
