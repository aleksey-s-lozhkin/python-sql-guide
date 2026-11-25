-- Глава 22: подзапросы и CTE. База: learning_shop.

-- 1. Скалярный подзапрос: средняя выручка заказа
SELECT ROUND(AVG(quantity * price), 2) AS avg_revenue
FROM orders o JOIN products p ON p.id = o.product_id;

-- 2. Заказы выше средней выручки
SELECT o.id, (o.quantity * p.price) AS revenue
FROM orders o JOIN products p ON p.id = o.product_id
WHERE (o.quantity * p.price) > (
    SELECT AVG(o2.quantity * p2.price)
    FROM orders o2 JOIN products p2 ON p2.id = o2.product_id
)
ORDER BY revenue DESC;

-- 3. NOT EXISTS: заказы без пользователя
SELECT o.id, o.created_at
FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM users u WHERE u.id = o.user_id);

-- 4. CTE: выручка по пользователям
WITH order_revenue AS (
    SELECT o.id, o.user_id, o.quantity * p.price AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
),
user_totals AS (
    SELECT user_id, SUM(revenue) AS total
    FROM order_revenue
    GROUP BY user_id
)
SELECT u.name, t.total
FROM user_totals t JOIN users u ON u.id = t.user_id
ORDER BY t.total DESC;

-- 5. CTE: выручка по месяцам
WITH monthly AS (
    SELECT DATE_TRUNC('month', o.created_at)::date AS month,
           SUM(o.quantity * p.price) AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
    GROUP BY 1
)
SELECT * FROM monthly ORDER BY month;

-- 6. CTE: категория с максимальной выручкой
WITH category_revenue AS (
    SELECT p.category, SUM(o.quantity * p.price) AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
    GROUP BY p.category
)
SELECT category, revenue
FROM category_revenue
ORDER BY revenue DESC
LIMIT 1;

-- 7. Коррелированный подзапрос в SELECT
SELECT u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS orders
FROM users u ORDER BY u.id;

-- 8. Рекурсивный CTE: числа 1..5
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 5
)
SELECT * FROM numbers;
