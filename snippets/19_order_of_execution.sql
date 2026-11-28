-- Глава 19: порядок выполнения запроса.
-- База: learning_shop (см. tools/setup_db.sh)

-- 1. Алиас в WHERE не виден: SELECT ещё не выполнен
SELECT price * 1.2 AS price_with_tax
FROM products
WHERE price_with_tax > 1000;
-- ERROR: column "price_with_tax" does not exist

-- 2. Алиас в ORDER BY работает: ORDER BY идёт после SELECT
SELECT name, price * 1.2 AS price_with_tax
FROM products
ORDER BY price_with_tax DESC
LIMIT 3;

-- 3. WHERE фильтрует строки, HAVING — группы
SELECT category, COUNT(*) AS cnt
FROM products
WHERE price > 500
GROUP BY category
HAVING COUNT(*) >= 2;

-- 4. Полный конвейер: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
SELECT category, COUNT(*) AS cnt, MAX(price) AS max_price
FROM products
WHERE price > 400
GROUP BY category
HAVING COUNT(*) > 1
ORDER BY cnt DESC
LIMIT 2;

-- 5. LIMIT без ORDER BY: порядок не гарантирован
SELECT name, price FROM products LIMIT 2;
