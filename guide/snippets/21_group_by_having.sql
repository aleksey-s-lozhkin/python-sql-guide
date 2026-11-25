-- Глава 21: GROUP BY и HAVING. База: learning_shop.

-- 1. Выручка и число заказов по пользователям
SELECT u.name, COUNT(*) AS orders, SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
ORDER BY revenue DESC;

-- 2. HAVING: только пользователи с несколькими заказами
SELECT u.name, COUNT(*) AS orders, SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
HAVING COUNT(*) > 1
ORDER BY revenue DESC;

-- 3. WHERE и HAVING вместе
SELECT p.category, COUNT(*) AS items, ROUND(SUM(o.quantity * p.price), 2) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
WHERE p.price > 400
GROUP BY p.category
HAVING SUM(o.quantity * p.price) > 3000
ORDER BY revenue DESC;

-- 4. Группировка по двум колонкам
SELECT p.category,
       DATE_TRUNC('month', o.created_at)::date AS month,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.category, DATE_TRUNC('month', o.created_at)
ORDER BY month, category;

-- 5. NULL как группа и COUNT
SELECT o.user_id, COUNT(*) AS cnt
FROM orders o
GROUP BY o.user_id
ORDER BY o.user_id NULLS LAST;

SELECT COUNT(*) AS rows, COUNT(user_id) AS known_user FROM orders;

-- 6. Агрегаты игнорируют NULL
SELECT COUNT(*) AS rows, COUNT(city) AS cities,
       COUNT(DISTINCT city) AS unique_cities
FROM users;
