"""Справочная лаборатория: pandas merge.

Требуется pandas 3.0.1 (как в книге).
Запуск: python3 guide/snippets/ref_pd_merge_lab.py
"""
import numpy as np
import pandas as pd

# ─── 1. Данные: заказы и пользователи ────────────────────────────
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "user_id": [10, 20, 10, 40, 10],
    "amount": [1200, 800, 500, 2100, 300],
})
users = pd.DataFrame({
    "user_id": [10, 20, 30],
    "name": ["Anna", "Ivan", "Olga"],
    "city": ["Москва", "Казань", "Москва"],
})
print(orders)
print(users)

# ─── 2. Четыре типа соединения ───────────────────────────────────
for how in ["inner", "left", "right", "outer"]:
    merged = orders.merge(users, on="user_id", how=how)
    print(f"{how:5} {len(merged)} rows")
print(orders.merge(users, on="user_id"))

# ─── 3. indicator: откуда пришла строка ──────────────────────────
left = orders.merge(users, on="user_id", how="left", indicator=True)
print(left[["order_id", "user_id", "name", "_merge"]])
print(left["_merge"].value_counts())

# ─── 4. validate: проверка кардинальности ────────────────────────
try:
    users.merge(orders, on="user_id", validate="one_to_one")
except pd.errors.MergeError as err:
    print("MergeError:", str(err).splitlines()[0])

# ─── 5. Суффиксы и разные имена ключей ───────────────────────────
limits = pd.DataFrame({"user_id": [10], "amount": [5000]})
print(orders.merge(limits, on="user_id", how="left").columns.tolist())
print(orders.merge(limits, on="user_id", how="left", suffixes=("_order", "_limit")))

buyers = pd.DataFrame({"order_id": [1, 2], "buyer": [10, 20]})
clients = pd.DataFrame({"client_id": [10, 20], "name": ["Anna", "Ivan"]})
print(buyers.merge(clients, left_on="buyer", right_on="client_id"))

# ─── 6. join по индексу и concat ─────────────────────────────────
by_id = users.set_index("user_id")
print(orders.set_index("user_id").join(by_id, how="left"))

more = pd.DataFrame({"order_id": [6], "user_id": [20], "amount": [400]})
print(pd.concat([orders, more], ignore_index=True))
status = pd.DataFrame({"status": ["paid", "paid", "new", "paid", "new"]})
print(pd.concat([orders, status], axis=1))

# ─── 7. Кардинальность: many-to-many ─────────────────────────────
a = pd.DataFrame({"user_id": [10, 10], "order_id": [1, 2]})
b = pd.DataFrame({"user_id": [10, 10], "city": ["Москва", "Казань"]})
print(a.merge(b, on="user_id"))
print("rows:", len(a.merge(b, on="user_id")), "ожидание: 2 × 2 = 4")

# ─── 8. Ключи: разные типы и NaN ─────────────────────────────────
users_str = users.assign(user_id=users["user_id"].astype(str))
try:
    orders.merge(users_str, on="user_id")
except ValueError as err:
    print("ValueError:", str(err).splitlines()[0])

users_null = pd.concat(
    [users, pd.DataFrame({"user_id": [np.nan], "name": ["гость"], "city": ["—"]})],
    ignore_index=True,
)
orders_null = pd.DataFrame({"user_id": [10, None], "amount": [100, 200]})
print(orders_null.merge(users_null, on="user_id", how="left", indicator=True))

# ─── 9. Сценарий: заказы + пользователи ──────────────────────────
enriched = orders.merge(users, on="user_id", how="left", validate="many_to_one")
print(enriched[["order_id", "name", "amount"]])

# ─── 10. Сценарий: пользователи без заказов ──────────────────────
joined = users.merge(orders, on="user_id", how="left", indicator=True)
print(joined[["user_id", "name", "_merge"]])

# ─── 11. Сценарий: дедупликация после merge ──────────────────────
users_dup = pd.concat(
    [users, pd.DataFrame({"user_id": [10], "name": ["Anna (old)"], "city": ["Москва"]})],
    ignore_index=True,
)
inflated = orders.merge(users_dup, on="user_id", how="left")
print("rows:", len(inflated), "expected:", len(orders))
clean = users_dup.drop_duplicates("user_id", keep="last")
print("rows after dedup:", len(orders.merge(clean, on="user_id", how="left")))

# ─── 12. Мост: map для простого справочника ──────────────────────
names = users.set_index("user_id")["name"]
print(orders["user_id"].map(names))
