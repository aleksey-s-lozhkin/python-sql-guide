"""Глава 26, шаг 6: динамика выручки по месяцам в pandas.

Сначала выгрузите месячную сводку из PostgreSQL в CSV:

    psql -d learning_shop -c "\\copy (
        WITH order_revenue AS (
            SELECT o.id, o.created_at, o.quantity * p.price AS revenue
            FROM orders o JOIN products p ON p.id = o.product_id
        )
        SELECT DATE_TRUNC('month', created_at)::date AS month,
               COUNT(*) AS orders,
               SUM(revenue) AS revenue,
               ROUND(AVG(revenue), 2) AS avg_check
        FROM order_revenue GROUP BY 1 ORDER BY 1
    ) TO '/tmp/monthly.csv' CSV HEADER"

Запуск:  python3 guide/snippets/26_project.py
"""
import pandas as pd

df = pd.read_csv("/tmp/monthly.csv")
df["growth_pct"] = (df["revenue"].pct_change() * 100).round(1)

print(df.to_string(index=False))
print("total revenue:", df["revenue"].sum(), "| orders:", df["orders"].sum())
