-- Справочник: GROUP BY и HAVING (SQL, страница 3 из 6). База: learning_shop.
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_group_lab.sql
-- Только SELECT: данные не меняются.

-- 1. Шаблон: одна колонка-ключ и COUNT
SELECT u.city, COUNT(*) AS users
FROM users u
GROUP BY u.city
ORDER BY users DESC, u.city;

-- 2. Пять агрегатов по одной колонке
SELECT p.category,
       COUNT(*) AS orders,
       SUM(o.quantity) AS items,
       ROUND(AVG(o.quantity * p.price), 2) AS avg_check,
       MIN(p.price) AS min_price,
       MAX(p.price) AS max_price
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.category
ORDER BY p.category;

-- 3. Два ключа: категория и месяц
SELECT p.category,
       DATE_TRUNC('month', o.created_at)::date AS month,
       COUNT(*) AS orders,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.category, DATE_TRUNC('month', o.created_at)
ORDER BY month, p.category;

-- 4. GROUP BY по выражению: CASE-корзина по цене
SELECT CASE WHEN p.price >= 10000 THEN 'дорогой'
            ELSE 'дешёвый' END AS price_tier,
       COUNT(*) AS orders,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY CASE WHEN p.price >= 10000 THEN 'дорогой'
              ELSE 'дешёвый' END
ORDER BY revenue DESC;

-- 5. WHERE и HAVING в одном запросе
SELECT p.category,
       COUNT(*) AS orders,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
WHERE p.price > 400
GROUP BY p.category
HAVING SUM(o.quantity * p.price) > 3000
ORDER BY revenue DESC;

-- 6. FILTER: условный агрегат в одной строке
SELECT p.category,
       COUNT(*) AS orders,
       COUNT(*) FILTER (WHERE o.created_at >= DATE '2024-03-01') AS march_orders,
       SUM(o.quantity * p.price)
           FILTER (WHERE o.created_at < DATE '2024-02-01') AS jan_revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.category
ORDER BY p.category;

-- 7. COUNT(*) против COUNT(col) и NULL-группа
SELECT u.city,
       COUNT(*) AS users,
       COUNT(u.email) AS with_email
FROM users u
GROUP BY u.city
ORDER BY u.city NULLS LAST;

-- 8. ORDER BY агрегата, алиас и доля группы
SELECT p.category,
       SUM(o.quantity * p.price) AS revenue,
       ROUND(100.0 * SUM(o.quantity * p.price)
             / SUM(SUM(o.quantity * p.price)) OVER (), 1) AS share_pct
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 9. Сценарий: выручка и число заказов по пользователям
SELECT u.name, COUNT(*) AS orders, SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
ORDER BY revenue DESC;

-- 10. Сценарий: заказы и выручка по месяцам
SELECT DATE_TRUNC('month', o.created_at)::date AS month,
       COUNT(*) AS orders,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY DATE_TRUNC('month', o.created_at)
ORDER BY month;

-- 11. Сценарий: HAVING с порогом выручки
SELECT u.name, COUNT(*) AS orders, SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY u.name
HAVING SUM(o.quantity * p.price) > 50000
ORDER BY revenue DESC;

-- 12. Задача: категории с выручкой больше 10000
SELECT p.category, COUNT(*) AS orders, SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.category
HAVING SUM(o.quantity * p.price) > 10000
ORDER BY revenue DESC;

-- 13. Задача: выручка по пользователям вместе с гостевым заказом
SELECT COALESCE(u.name, 'гость') AS who,
       COUNT(*) AS orders,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
GROUP BY COALESCE(u.name, 'гость')
ORDER BY revenue DESC;
