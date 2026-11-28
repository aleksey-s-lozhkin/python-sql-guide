"""Глава 25: тот же агрегат в pandas.

Выгрузка из базы:
    psql -d learning_shop -c "\\copy (SELECT o.user_id, o.quantity, p.price
        FROM orders_big o JOIN products p ON p.id = o.product_id)
        TO '/tmp/big_orders.csv' CSV HEADER"

Запуск:  python3 guide/snippets/25_benchmark.py
"""
import time

import pandas as pd

t0 = time.perf_counter()
df = pd.read_csv("/tmp/big_orders.csv")
t_read = time.perf_counter() - t0

t0 = time.perf_counter()
df["revenue"] = df["quantity"] * df["price"]
result = df.groupby("user_id")["revenue"].sum()
t_calc = time.perf_counter() - t0

print("rows:", len(df))
print("read_csv: %.1f ms" % (t_read * 1000))
print("groupby:  %.1f ms" % (t_calc * 1000))
print("total:    %.1f ms" % ((t_read + t_calc) * 1000))
print(result.astype("int64").to_string())
