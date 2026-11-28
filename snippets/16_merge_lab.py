"""Лаборатория к главе 16: merge.

Запуск:  python3 guide/snippets/16_merge_lab.py
"""
import numpy as np
import pandas as pd

print("pandas", pd.__version__)
print("=" * 64)

orders = pd.DataFrame(
    {"order_id": [1, 2, 3, 4], "user_id": [10, 20, 10, 30], "amount": [1200, 800, 500, 2100]}
)
users = pd.DataFrame({"user_id": [10, 20, 40], "name": ["anna", "ivan", "olga"]})
print("orders:\n", orders)
print("users:\n", users)

# ─── 1. Четыре типа соединения ───────────────────────────────────
print("\n1) INNER, LEFT, RIGHT, OUTER")
print("   inner:\n", orders.merge(users, on="user_id", how="inner"))
print("   left:\n", orders.merge(users, on="user_id", how="left"))
print("   right:\n", orders.merge(users, on="user_id", how="right"))
print("   outer:\n", orders.merge(users, on="user_id", how="outer"))

# ─── 2. indicator: что не совпало ────────────────────────────────
print("\n2) INDICATOR: ОТКУДА СТРОКА")
left = orders.merge(users, on="user_id", how="left", indicator=True)
print(left)
print("   counts:\n", left["_merge"].value_counts())

# ─── 3. validate: защита от неожиданной кардинальности ───────────
print("\n3) VALIDATE: ЛОВИМ ДУБЛИ КЛЮЧЕЙ")
users_dup = pd.concat([users, pd.DataFrame({"user_id": [10], "name": ["anna_2"]})])
print("   users_dup:\n", users_dup)
try:
    orders.merge(users_dup, on="user_id", validate="one_to_one")
except pd.errors.MergeError as e:
    print("   MergeError:", str(e).split("\n")[0])

# ─── 4. many-to-many: строки размножаются ───────────────────────
print("\n4) MANY-TO-MANY: 2 × 2 = 4 СТРОКИ")
a = pd.DataFrame({"user_id": [10, 10], "order_id": [1, 2]})
b = pd.DataFrame({"user_id": [10, 10], "city": ["Москва", "Казань"]})
print(a.merge(b, on="user_id"))

# ─── 5. Суффиксы при совпадающих колонках ───────────────────────
print("\n5) СУФФИКСЫ")
left_tbl = pd.DataFrame({"user_id": [10], "amount": [100]})
right_tbl = pd.DataFrame({"user_id": [10], "amount": [200]})
print(left_tbl.merge(right_tbl, on="user_id", suffixes=("_order", "_limit")))

# ─── 6. concat: склейка без ключа ───────────────────────────────
print("\n6) CONCAT: СТРОКИ И КОЛОНКИ")
more_orders = pd.DataFrame({"order_id": [5], "user_id": [20], "amount": [300]})
print("   concat по строкам:\n", pd.concat([orders, more_orders], ignore_index=True))
print("   concat по колонкам:\n", pd.concat([orders.reset_index(drop=True), more_orders.reset_index(drop=True)], axis=1))

# ─── 7. Несовпадение типов ключей ───────────────────────────────
print("\n7) ТИПЫ КЛЮЧЕЙ ДОЛЖНЫ СОВПАДАТЬ")
users_str = users.assign(user_id=users["user_id"].astype(str))
try:
    orders.merge(users_str, on="user_id")
except ValueError as e:
    print("   ValueError:", str(e).split("\n")[0])

# ─── 8. NaN-ключи в pandas соединяются с NaN ────────────────────
print("\n8) NULL В КЛЮЧЕ: PANDAS СОЕДИНЯЕТ NaN С NaN (В ОТЛИЧИЕ ОТ SQL)")
users_null = pd.concat(
    [users, pd.DataFrame({"user_id": [np.nan], "name": ["гость"]})], ignore_index=True
)
orders_null = pd.DataFrame({"user_id": [10, None], "amount": [100, 200]})
print(orders_null.merge(users_null, on="user_id", how="left", indicator=True))
print("=" * 64)
