"""Справочная лаборатория: pandas groupby.

Требуется pandas 3.0.1 (как в книге).
Запуск: python3 guide/snippets/ref_pd_groupby_lab.py
"""
from collections import defaultdict

import pandas as pd

# ─── 1. Данные: одна строка = один заказ ─────────────────────────
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "user": ["Anna", "Ivan", "Anna", "Olga", "Ivan", "Ivan"],
    "city": ["Москва", "Казань", "Москва", "Казань", "Москва", "Казань"],
    "amount": [1200, 800, 500, 2100, 300, 400],
    "discount": [100.0, None, 50.0, None, 25.0, None],
})
print(orders)
print(orders.dtypes)

# ─── 2. Объект groupby ленивый ───────────────────────────────────
g = orders.groupby("user")
print(type(g).__name__)
print(g.size())

# ─── 3. Несколько ключей ─────────────────────────────────────────
print(orders.groupby(["city", "user"])["amount"].sum())

# ─── 4. Несколько агрегатов сразу ────────────────────────────────
print(orders.groupby("user")["amount"].agg(["sum", "mean", "median", "min", "max"]))

# ─── 5. size против count ────────────────────────────────────────
print(orders.groupby("user").size())
print(orders.groupby("user")["discount"].count())

# ─── 6. Именованная агрегация по разным колонкам ─────────────────
print(orders.groupby("user").agg(total=("amount", "sum"), orders=("order_id", "count")))

# ─── 7. as_index=False и сортировка ──────────────────────────────
print(orders.groupby("user", as_index=False)["amount"].sum())
print(orders.groupby("user")["amount"].sum().sort_values(ascending=False))

# ─── 8. transform против agg ─────────────────────────────────────
print(orders.groupby("user")["amount"].agg("mean").shape)
print(orders.groupby("user")["amount"].transform("mean").shape)
avg = orders.groupby("user")["amount"].transform("mean")
print(orders.assign(user_avg=avg))

# ─── 9. filter: оставить группы по условию ───────────────────────
print(orders.groupby("user").filter(lambda group: len(group) > 1))

# ─── 10. NaN в ключе и dropna ────────────────────────────────────
clicks = pd.DataFrame({"user": ["Anna", None, "Ivan", "Anna"], "clicks": [3, 1, 5, 2]})
print(clicks)
print(clicks.groupby("user").size())
print(clicks.groupby("user", dropna=False).size())

# ─── 11. Доли и value_counts ─────────────────────────────────────
share = orders.groupby("user")["amount"].sum() / orders["amount"].sum()
print(share.round(3))
print(orders["user"].value_counts())
print(orders.groupby("user").size())

# ─── 12. Сценарий: выручка по пользователю ───────────────────────
report = (
    orders.groupby("user", as_index=False)
    .agg(total=("amount", "sum"), orders=("order_id", "count"))
    .sort_values("total", ascending=False)
)
print(report)

# ─── 13. Сценарий: средний чек ───────────────────────────────────
print(orders.groupby("user")["amount"].mean().round(2))

# ─── 14. Сценарий: доля каждого в общей сумме ────────────────────
total = orders["amount"].sum()
shares = (orders.groupby("user")["amount"].sum() / total * 100).round(1)
print(shares)

# ─── 15. Мост: тот же итог руками, через defaultdict ─────────────
totals = defaultdict(int)
for user, amount in zip(orders["user"], orders["amount"]):
    totals[user] += amount
print(dict(totals))
print(orders.groupby("user")["amount"].sum().to_dict())
