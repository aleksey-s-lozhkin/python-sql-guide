-- Глава 20: SELECT, WHERE и логика трёх значений.
-- База: learning_shop (см. tools/setup_db.sh)
-- В users: у Petr нет города, у Maria нет email.

-- 1. DISTINCT: NULL — тоже отдельное значение
SELECT DISTINCT city FROM users ORDER BY city;

-- 2. = NULL не находит ничего
SELECT id, name FROM users WHERE city = NULL;

-- 3. IS NULL находит пропуск
SELECT id, name, city FROM users WHERE city IS NULL;

-- 4. <> не включает NULL
SELECT id, name, city FROM users WHERE city <> 'Москва';

-- 5. Три значения истины
SELECT NULL = NULL AS eq, NULL <> NULL AS neq,
       NULL AND true AS a, NULL OR false AS o;

-- 6. IN со NULL в списке
SELECT id, name, city FROM users WHERE city IN ('Москва', NULL);

-- 7. Ловушка NOT IN с NULL в подзапросе
SELECT id, name FROM users WHERE city NOT IN (SELECT city FROM users);

-- 8. COUNT(*) против COUNT(col)
SELECT COUNT(*) AS all_rows, COUNT(city) AS known_city FROM users;

-- 9. BETWEEN, LIKE, сортировка с NULL
SELECT name, price FROM products WHERE price BETWEEN 1000 AND 30000 ORDER BY price;
SELECT name FROM products WHERE name LIKE '%о%' ORDER BY name;
SELECT name, city FROM users ORDER BY city ASC NULLS LAST;

-- 10. COALESCE
SELECT name, COALESCE(city, 'неизвестно') AS city_filled FROM users;
