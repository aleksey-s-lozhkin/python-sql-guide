-- Справочник SQL, страница 2: JOIN.
-- База: learning_shop (PostgreSQL 14). Только SELECT.
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_join_lab.sql
--
-- Каждый блок начинается с \echo-маркера: по нему удобно сверять .out на странице.
-- Вывод psql настоящий; NULL печатается пустой ячейкой (так по умолчанию).

\echo '── 03a. INNER JOIN ──'
SELECT o.id AS order_id, u.name, o.quantity
FROM orders o
JOIN users u ON u.id = o.user_id
ORDER BY o.id;

\echo '── 05a. LEFT JOIN: все заказы ──'
SELECT o.id AS order_id, u.name, o.quantity
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
ORDER BY o.id;

\echo '── 05b. RIGHT и FULL: сколько строк ──'
SELECT 'inner' AS join_type, COUNT(*) AS rows
FROM orders o JOIN users u ON u.id = o.user_id
UNION ALL
SELECT 'left', COUNT(*)
FROM orders o LEFT JOIN users u ON u.id = o.user_id
UNION ALL
SELECT 'right', COUNT(*)
FROM orders o RIGHT JOIN users u ON u.id = o.user_id
UNION ALL
SELECT 'full', COUNT(*)
FROM orders o FULL JOIN users u ON u.id = o.user_id
ORDER BY join_type;

\echo '── 05c. NULL-ключ не соединяется ──'
SELECT id, user_id
FROM orders
WHERE user_id IS NULL;

SELECT COUNT(*) AS matched_rows
FROM orders o
JOIN users u ON u.id = o.user_id;

SELECT o.id AS order_id
FROM orders o
WHERE NOT EXISTS (
    SELECT 1
    FROM users u
    WHERE u.id = o.user_id
)
ORDER BY o.id;

\echo '── 05d. semi-join через EXISTS ──'
SELECT u.name
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    JOIN products p ON p.id = o.product_id
    WHERE o.user_id = u.id AND p.category = 'electronics'
)
ORDER BY u.name;

SELECT u.name
FROM users u
JOIN orders o ON o.user_id = u.id
JOIN products p ON p.id = o.product_id
WHERE p.category = 'electronics'
ORDER BY u.name, o.id;

\echo '── 05e. self-join и CROSS JOIN ──'
SELECT a.name AS user_a, b.name AS user_b, a.city
FROM users a
JOIN users b ON a.city = b.city AND a.id < b.id
ORDER BY a.name, b.name;

SELECT COUNT(*) AS cross_rows
FROM orders
CROSS JOIN users;

\echo '── 05f. фильтр в ON или в WHERE ──'
SELECT o.id AS order_id, u.name
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
WHERE u.city = 'Москва'
ORDER BY o.id;

SELECT o.id AS order_id, u.name
FROM orders o
LEFT JOIN users u ON u.id = o.user_id AND u.city = 'Москва'
ORDER BY o.id;

\echo '── 06a. Сценарий: заказы с именами ──'
SELECT o.id AS order_id,
       COALESCE(u.name, '—') AS user_name,
       o.quantity * p.price AS total
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY o.id;

\echo '── 06b. Сценарий: анти-джойн ──'
SELECT o.id AS order_id, o.created_at
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
WHERE u.id IS NULL;

SELECT u.name
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL
ORDER BY u.name;

\echo '── 06c. Сценарий: выручка по товарам ──'
SELECT p.name, p.category,
       SUM(o.quantity) AS units,
       SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p ON p.id = o.product_id
GROUP BY p.id, p.name, p.category
ORDER BY revenue DESC;

\echo '── 08a. Задача: заказы с товарами ──'
SELECT o.id AS order_id, p.name AS product, o.quantity,
       o.quantity * p.price AS total
FROM orders o
JOIN products p ON p.id = o.product_id
ORDER BY o.id;

\echo '── 08b. Задача: топ по сумме ──'
SELECT o.id AS order_id,
       COALESCE(u.name, '—') AS user_name,
       p.name AS product,
       o.quantity * p.price AS total
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
JOIN products p ON p.id = o.product_id
ORDER BY total DESC, o.id
LIMIT 4;
