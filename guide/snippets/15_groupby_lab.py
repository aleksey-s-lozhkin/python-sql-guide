"""Лаборатория к главе 15: groupby.

Запуск:  python3 guide/snippets/15_groupby_lab.py
"""
import pandas as pd

print("pandas", pd.__version__)
print("=" * 64)

orders = pd.DataFrame(
    {
        "user": ["anna", "ivan", "anna", "petr", "ivan"],
        "city": ["Москва", "Казань", "Москва", "Москва", "Казань"],
        "amount": [1200, 800, 500, 2100, 300],
    }
)
print("orders:\n", orders)

# ─── 1. Разложить по ключу ──────────────────────────────────────
print("\n1) РАЗЛОЖИТЬ: GROUPBY ПО КЛЮЧУ")
g = orders.groupby("user")
print("   тип:", type(g).__name__)
print("   size (строк в группе):\n", g.size())

# ─── 2. Посчитать: агрегаты ─────────────────────────────────────
print("\n2) ПОСЧИТАТЬ: SUM, COUNT, MEAN")
print("   sum:\n", g["amount"].sum())
print("   agg(['count','sum','mean']):\n", g["amount"].agg(["count", "sum", "mean"]))

# ─── 3. Собрать: as_index=False ─────────────────────────────────
print("\n3) СОБРАТЬ: ОБЫЧНАЯ ТАБЛИЦА")
print(orders.groupby("user", as_index=False)["amount"].sum())

# ─── 4. Именованная агрегация ───────────────────────────────────
print("\n4) ИМЕНОВАННАЯ АГРЕГАЦИЯ")
summary = orders.groupby("user").agg(
    total=("amount", "sum"),
    orders=("amount", "count"),
    avg=("amount", "mean"),
)
print(summary)

# ─── 5. Несколько ключей ────────────────────────────────────────
print("\n5) НЕСКОЛЬКО КЛЮЧЕЙ")
print(orders.groupby(["city", "user"])["amount"].sum())

# ─── 6. transform: результат той же длины ───────────────────────
print("\n6) TRANSFORM: ДОБАВИТЬ СРЕДНЕЕ ПО ГРУППЕ К КАЖДОЙ СТРОКЕ")
orders["user_avg"] = orders.groupby("user")["amount"].transform("mean")
print(orders)

# ─── 7. filter: оставить группы по условию ──────────────────────
print("\n7) FILTER: ОСТАВИТЬ ТОЛЬКО «КРУПНЫЕ» ГРУППЫ")
big = orders.groupby("user").filter(lambda group: group["amount"].sum() > 1500)
print(big)

# ─── 8. Сравнение с dict-аккумулятором ─────────────────────────
print("\n8) ТО ЖЕ САМОЕ РУКАМИ (ГЛАВА 02)")
from collections import defaultdict

totals = defaultdict(int)
for user, amount in zip(orders["user"], orders["amount"]):
    totals[user] += amount
print("   dict:", dict(totals))
print("   groupby:\n", orders.groupby("user")["amount"].sum().to_dict())

# ─── 9. Сортировка результата ───────────────────────────────────
print("\n9) ТОП ПО СУММЕ")
print(orders.groupby("user")["amount"].sum().sort_values(ascending=False))
print("=" * 64)
