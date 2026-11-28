-- Справочник: оконные функции (SQL, страница 4 из 6). База: learning_shop.
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_window_lab.sql
-- Только SELECT: данные не меняются.

-- 1. Шаблон: SUM OVER (PARTITION BY ... ORDER BY ...)
SELECT o.id, o.quantity * p.price AS revenue,
       SUM(o.quantity * p.price) OVER (
           PARTITION BY o.user_id
           ORDER BY o.created_at
       ) AS running
FROM orders o
JOIN products p ON p.id = o.product_id
WHERE o.user_id = 1
ORDER BY o.id;

-- 2. OVER (): итог и среднее рядом с каждой строкой
SELECT o.id, (o.quantity * p.price) AS revenue,
       SUM(o.quantity * p.price) OVER () AS total_all,
       ROUND(AVG(o.quantity * p.price) OVER (), 2) AS avg_all
FROM orders o
JOIN products p ON p.id = o.product_id
ORDER BY o.id;

-- 3. PARTITION BY: сумма по пользователю рядом с каждым заказом
SELECT o.id, u.name, (o.quantity * p.price) AS revenue,
       SUM(o.quantity * p.price) OVER (PARTITION BY o.user_id) AS user_total
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY u.name, o.id;

-- 4. ORDER BY и накопительная сумма (рамка по умолчанию)
SELECT o.id, o.created_at::date AS day, (o.quantity * p.price) AS revenue,
       SUM(o.quantity * p.price) OVER (ORDER BY o.created_at, o.id) AS running_all
FROM orders o
JOIN products p ON p.id = o.product_id
ORDER BY o.created_at, o.id;

-- 5. ROW_NUMBER, RANK и DENSE_RANK при равенстве выручки
SELECT o.id, (o.quantity * p.price) AS revenue,
       ROW_NUMBER() OVER (ORDER BY o.quantity * p.price DESC, o.id) AS rn,
       RANK()       OVER (ORDER BY o.quantity * p.price DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY o.quantity * p.price DESC) AS dense
FROM orders o
JOIN products p ON p.id = o.product_id
ORDER BY o.quantity * p.price DESC, o.id;

-- 6. LAG и LEAD: соседние заказы пользователя
SELECT u.name, o.id, o.created_at::date AS day,
       (o.quantity * p.price) AS revenue,
       LAG(o.quantity * p.price) OVER (
           PARTITION BY o.user_id ORDER BY o.created_at, o.id
       ) AS prev,
       LEAD(o.quantity * p.price) OVER (
           PARTITION BY o.user_id ORDER BY o.created_at, o.id
       ) AS next
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY u.name, o.created_at, o.id;

-- 7. Рамка ROWS BETWEEN: сумма текущей и предыдущей строки
SELECT u.name, o.id, (o.quantity * p.price) AS revenue,
       SUM(o.quantity * p.price) OVER (
           PARTITION BY o.user_id
           ORDER BY o.created_at, o.id
           ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
       ) AS last_two
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY u.name, o.created_at, o.id;

-- 8. Доля строки в общей сумме окна
SELECT o.id, u.name, (o.quantity * p.price) AS revenue,
       ROUND(100.0 * (o.quantity * p.price)
             / SUM(o.quantity * p.price) OVER (), 1) AS share_pct
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY revenue DESC, o.id;

-- 9. Сценарий: топ-1 заказ на пользователя
WITH ranked AS (
    SELECT u.name, o.id, o.created_at::date AS day,
           (o.quantity * p.price) AS revenue,
           ROW_NUMBER() OVER (
               PARTITION BY o.user_id
               ORDER BY o.quantity * p.price DESC, o.id
           ) AS rn
    FROM orders o
    JOIN users u ON u.id = o.user_id
    JOIN products p ON p.id = o.product_id
)
SELECT name, id, day, revenue
FROM ranked
WHERE rn = 1
ORDER BY name;

-- 10. Сценарий: накопительная выручка по месяцам
SELECT DATE_TRUNC('month', o.created_at)::date AS month,
       SUM(o.quantity * p.price) AS month_revenue,
       SUM(SUM(o.quantity * p.price)) OVER (
           ORDER BY DATE_TRUNC('month', o.created_at)
       ) AS running
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY DATE_TRUNC('month', o.created_at)
ORDER BY month;

-- 11. Сценарий: доля пользователя в общей выручке
SELECT u.name,
       SUM(o.quantity * p.price) AS revenue,
       SUM(SUM(o.quantity * p.price)) OVER () AS total_revenue,
       ROUND(100.0 * SUM(o.quantity * p.price)
             / SUM(SUM(o.quantity * p.price)) OVER (), 1) AS share_pct
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
ORDER BY revenue DESC;

-- 12. Задача: топ-2 заказа на пользователя
WITH ranked AS (
    SELECT u.name, o.id, (o.quantity * p.price) AS revenue,
           ROW_NUMBER() OVER (
               PARTITION BY o.user_id
               ORDER BY o.quantity * p.price DESC, o.id
           ) AS rn
    FROM orders o
    JOIN users u ON u.id = o.user_id
    JOIN products p ON p.id = o.product_id
)
SELECT name, id, revenue
FROM ranked
WHERE rn <= 2
ORDER BY name, revenue DESC;

-- 13. Задача: разница с предыдущим заказом пользователя (LAG)
SELECT u.name, o.created_at::date AS day, (o.quantity * p.price) AS revenue,
       (o.quantity * p.price)
       - LAG(o.quantity * p.price) OVER (
           PARTITION BY o.user_id ORDER BY o.created_at, o.id
       ) AS delta
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY u.name, o.created_at, o.id;
