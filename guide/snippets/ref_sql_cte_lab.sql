-- Справочник: подзапросы и CTE. Все примеры страницы ref-sql-cte.html.
--
-- Запуск из корня проекта:
--     psql -d learning_shop -f guide/snippets/ref_sql_cte_lab.sql
--
-- Только SELECT и EXPLAIN: лаборатория ничего не меняет в базе.
-- Вывод детерминирован: везде явный ORDER BY, планы — без ANALYZE.

\echo '== 03.1 Скалярный подзапрос: средняя выручка =='
SELECT ROUND(AVG(quantity * price), 2) AS avg_revenue
FROM orders o JOIN products p ON p.id = o.product_id;

\echo '== 03.2 CTE: шаблон =='
WITH user_totals AS (
    SELECT user_id, SUM(quantity * price) AS total
    FROM orders o JOIN products p ON p.id = o.product_id
    GROUP BY user_id
)
SELECT u.name, t.total
FROM user_totals t JOIN users u ON u.id = t.user_id
ORDER BY t.total DESC, u.name;

\echo '== 05.1 Скалярный подзапрос в WHERE =='
SELECT o.id, (o.quantity * p.price) AS revenue
FROM orders o JOIN products p ON p.id = o.product_id
WHERE (o.quantity * p.price) > (
    SELECT AVG(quantity * price) FROM orders o2
    JOIN products p2 ON p2.id = o2.product_id
)
ORDER BY revenue DESC, o.id;

\echo '== 05.2 IN и ANY =='
SELECT id, name FROM users
WHERE id IN (SELECT user_id FROM orders WHERE quantity >= 3)
ORDER BY id;

SELECT id, name FROM users
WHERE id = ANY (ARRAY[1, 3])
ORDER BY id;

\echo '== 05.3 EXISTS и NOT EXISTS =='
SELECT u.id, u.name
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id)
ORDER BY u.id;

SELECT o.id, o.created_at
FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM users u WHERE u.id = o.user_id);

\echo '== 05.4 Коррелированный подзапрос =='
SELECT u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS orders
FROM users u
ORDER BY u.id;

\echo '== 05.5 Несколько CTE: агрегат, потом фильтр =='
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
WHERE t.total > 30000
ORDER BY t.total DESC, u.name;

\echo '== 05.6 CTE поверх CTE =='
WITH order_revenue AS (
    SELECT o.id, o.user_id, o.quantity * p.price AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
),
user_totals AS (
    SELECT user_id, SUM(revenue) AS total
    FROM order_revenue
    GROUP BY user_id
),
big_spenders AS (
    SELECT user_id, total FROM user_totals WHERE total > 50000
)
SELECT u.name, b.total
FROM big_spenders b JOIN users u ON u.id = b.user_id
ORDER BY b.total DESC, u.name;

\echo '== 05.7 Рекурсивный CTE: числа 1..5 =='
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 5
)
SELECT n FROM numbers;

\echo '== 05.8 План: CTE встраивается =='
EXPLAIN
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
ORDER BY t.total DESC, u.name;

\echo '== 05.9 План: MATERIALIZED =='
EXPLAIN
WITH order_revenue AS MATERIALIZED (
    SELECT o.id, o.user_id, o.quantity * p.price AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
),
user_totals AS MATERIALIZED (
    SELECT user_id, SUM(revenue) AS total
    FROM order_revenue
    GROUP BY user_id
)
SELECT u.name, t.total
FROM user_totals t JOIN users u ON u.id = t.user_id
ORDER BY t.total DESC, u.name;

\echo '== 06.1 Сценарий: выше средней выручки =='
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
WHERE t.total > (SELECT AVG(total) FROM user_totals)
ORDER BY t.total DESC, u.name;

\echo '== 06.2 Сценарий: не покупали в феврале =='
SELECT u.id, u.name
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
      AND o.created_at >= '2024-02-01'
      AND o.created_at < '2024-03-01'
)
ORDER BY u.id;

\echo '== 06.3 Сценарий: календарь месяцев =='
WITH RECURSIVE months AS (
    SELECT DATE '2024-01-01' AS month
    UNION ALL
    SELECT (month + INTERVAL '1 month')::date FROM months
    WHERE month < DATE '2024-06-01'
),
monthly AS (
    SELECT DATE_TRUNC('month', o.created_at)::date AS month,
           SUM(o.quantity * p.price) AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
    GROUP BY 1
)
SELECT m.month, COALESCE(mo.revenue, 0) AS revenue
FROM months m LEFT JOIN monthly mo ON mo.month = m.month
ORDER BY m.month;

\echo '== 07.1 NOT IN с NULL =='
SELECT id, name FROM users
WHERE id NOT IN (2, 4, NULL)
ORDER BY id;

\echo '== 07.2 NOT IN без NULL =='
SELECT id, name FROM users
WHERE id NOT IN (2, 4)
ORDER BY id;

\echo '== 08.1 Задача: меньше двух заказов =='
WITH user_orders AS (
    SELECT u.id, u.name, COUNT(o.id) AS orders
    FROM users u LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.name
)
SELECT name, orders
FROM user_orders
WHERE orders < 2
ORDER BY id;

\echo '== 08.2 Задача: категории выше средней =='
WITH category_revenue AS (
    SELECT p.category, SUM(o.quantity * p.price) AS revenue
    FROM orders o JOIN products p ON p.id = o.product_id
    GROUP BY p.category
)
SELECT category, revenue
FROM category_revenue
WHERE revenue > (SELECT AVG(revenue) FROM category_revenue)
ORDER BY revenue DESC;
