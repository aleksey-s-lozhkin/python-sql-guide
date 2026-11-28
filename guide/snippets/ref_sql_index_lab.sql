-- Справочник: индексы и EXPLAIN. Все примеры страницы ref-sql-index.html.
--
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_index_lab.sql
--
-- Только SELECT и EXPLAIN: лаборатория ничего не меняет в базе и не создаёт индексов.
-- Планы сняты без ANALYZE, чтобы вывод не зависел от времени выполнения.
-- Числа cost и rows зависят от статистики: на другой машине они могут отличаться.

\echo '== 03.1 EXPLAIN и поиск по первичному ключу =='
EXPLAIN SELECT * FROM orders_big WHERE id = 4242;

\echo '== 05.1 Seq Scan: подходящего индекса нет =='
EXPLAIN SELECT * FROM orders_big WHERE quantity = 2;

\echo '== 05.2 Index Scan: узкий диапазон дат =='
EXPLAIN SELECT * FROM orders_big
WHERE created_at >= '2024-01-02' AND created_at < '2024-01-03';

\echo '== 05.3 Bitmap Heap Scan: 20% строк =='
EXPLAIN SELECT * FROM orders_big
WHERE user_id = 3 AND quantity = 2;

\echo '== 05.4 Index Only Scan: индекс покрывает запрос =='
EXPLAIN SELECT user_id FROM orders_big WHERE user_id = 3;

\echo '== 05.5 Index Scan Backward: порядок и LIMIT =='
EXPLAIN SELECT * FROM orders_big
WHERE created_at >= '2024-03-01'
ORDER BY created_at DESC
LIMIT 10;

\echo '== 05.6 Функция и приведение ломают индекс =='
EXPLAIN SELECT * FROM orders_big
WHERE created_at::date = DATE '2024-01-02';

EXPLAIN SELECT * FROM orders_big WHERE id::text = '4242';

\echo '== 05.7 JOIN-план =='
EXPLAIN SELECT o.id, u.name
FROM orders_big o JOIN users u ON u.id = o.user_id
WHERE o.user_id = 3;

\echo '== 05.8 Низкая селективность: индекс не нужен =='
EXPLAIN SELECT * FROM orders_big WHERE user_id BETWEEN 1 AND 5;

\echo '== 06.1 Сценарий: заказы пользователя =='
EXPLAIN SELECT * FROM orders_big WHERE user_id = 3;

\echo '== 06.2 Сценарий: последние 10 заказов =='
EXPLAIN SELECT * FROM orders_big
ORDER BY created_at DESC
LIMIT 10;

\echo '== 06.3 Сценарий: отчёт по пользователям =='
EXPLAIN SELECT u.name, COUNT(*) AS orders
FROM orders_big o JOIN users u ON u.id = o.user_id
GROUP BY u.name
ORDER BY orders DESC, u.name;

\echo '== 08.1 Задача: диапазон января =='
EXPLAIN SELECT * FROM orders_big
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-15';

\echo '== 08.2 Задача: последние 10 заказов пользователя 3 =='
EXPLAIN SELECT * FROM orders_big
WHERE user_id = 3
ORDER BY created_at DESC
LIMIT 10;
