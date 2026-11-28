-- Справочник SQL, страница 1: SELECT, WHERE, NULL, ORDER BY.
-- База: learning_shop (PostgreSQL 14). Только SELECT.
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_select_lab.sql
--
-- Каждый блок начинается с \echo-маркера: по нему удобно сверять .out на странице.
-- Вывод psql настоящий; NULL печатается пустой ячейкой (так по умолчанию).

\echo '── 03a. Каркас запроса ──'
SELECT name, city, email
FROM users
WHERE city IS NOT NULL
ORDER BY name
LIMIT 3;

\echo '── 03b. Алиас в ORDER BY ──'
SELECT name, price * 1.2 AS price_with_tax
FROM products
ORDER BY price_with_tax DESC, name
LIMIT 3;

\echo '── 05a. DISTINCT и NULL ──'
SELECT DISTINCT city
FROM users
ORDER BY city;

\echo '── 05b. WHERE: = NULL, IS NULL, <> ──'
SELECT id, name
FROM users
WHERE city = NULL;

SELECT id, name, city
FROM users
WHERE city IS NULL;

SELECT name, city
FROM users
WHERE city <> 'Москва'
ORDER BY name;

\echo '── 05c. IN и NOT IN с NULL ──'
SELECT name, city
FROM users
WHERE city IN ('Москва', 'Казань')
ORDER BY name;

SELECT name, city
FROM users
WHERE city IN ('Москва', NULL)
ORDER BY name;

SELECT name
FROM users
WHERE city NOT IN (SELECT city FROM users)
ORDER BY name;

\echo '── 05d. BETWEEN и LIKE/ILIKE ──'
SELECT name, price
FROM products
WHERE price BETWEEN 1000 AND 30000
ORDER BY price;

SELECT name
FROM users
WHERE city LIKE '%москва%'
ORDER BY name;

SELECT name
FROM users
WHERE city ILIKE '%москва%'
ORDER BY name;

\echo '── 05e. ORDER BY, NULLS, LIMIT ──'
SELECT name, city
FROM users
ORDER BY city ASC NULLS FIRST, name;

SELECT name, city
FROM users
ORDER BY city DESC NULLS LAST, name
LIMIT 3;

\echo '── 05f. CASE, COALESCE, COUNT ──'
SELECT name,
       COALESCE(city, 'неизвестно') AS city_filled,
       CASE WHEN city IS NULL THEN 'нет данных' ELSE city END AS city_case
FROM users
ORDER BY id;

SELECT COUNT(*) AS all_rows,
       COUNT(city) AS known_city,
       COUNT(email) AS known_email
FROM users;

\echo '── 06a. Сценарий: город с пропусками ──'
SELECT name, city
FROM users
WHERE city <> 'Москва' OR city IS NULL
ORDER BY name;

\echo '── 06b. Сценарий: поиск по названию ──'
SELECT name, category, price
FROM products
WHERE name ILIKE '%о%'
ORDER BY price DESC;

\echo '── 06c. Сценарий: топ-N с сортировкой ──'
SELECT id, name, price
FROM products
ORDER BY price DESC, name
LIMIT 3;

\echo '── 08a. Задача: без города ──'
SELECT name, email
FROM users
WHERE city IS NULL
ORDER BY name;

\echo '── 08b. Задача: три последних заказа ──'
SELECT id, created_at, quantity
FROM orders
ORDER BY created_at DESC, id
LIMIT 3;
