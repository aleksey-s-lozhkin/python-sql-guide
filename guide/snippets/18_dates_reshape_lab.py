"""Лаборатория к главе 18: даты, строки и форма таблицы.

Запуск:  python3 guide/snippets/18_dates_reshape_lab.py
"""
import pandas as pd

print("pandas", pd.__version__)
print("=" * 64)

# ─── 1. Даты как строки и как datetimes ─────────────────────────
print("\n1) TO_DATETIME: ИЗ СТРОКИ В ДАТУ")
orders = pd.DataFrame(
    {
        "date": ["2024-01-05", "2024-02-10", "2024-02-15", "2024-03-01"],
        "user": ["anna", "ivan", "anna", "olga"],
        "amount": [1200, 800, 500, 2100],
    }
)
orders["date"] = pd.to_datetime(orders["date"])
print(orders)
print("   dtype:", orders["date"].dtype)

# ─── 2. Аксессор .dt ────────────────────────────────────────────
print("\n2) ДОСТУП К ЧАСТЯМ ДАТЫ")
print("   year :", orders["date"].dt.year.tolist())
print("   month:", orders["date"].dt.month.tolist())
print("   day  :", orders["date"].dt.day.tolist())
print("   месяц словом:", orders["date"].dt.month_name().tolist())

# ─── 3. Месяц как период и группировка ──────────────────────────
print("\n3) МЕСЯЦ КАК ПЕРИОД: ВЫРУЧКА ПО МЕСЯЦАМ")
orders["month"] = orders["date"].dt.to_period("M")
print(orders.groupby("month")["amount"].sum())

# ─── 4. Строки: .str ────────────────────────────────────────────
print("\n4) СТРОКИ: НОРМАЛИЗАЦИЯ И ПОИСК")
users = pd.DataFrame({"email": [" Anna@Mail.RU ", "ivan@mail.ru", None]})
print("   исходные:", users["email"].tolist())
print("   strip+lower:", users["email"].str.strip().str.lower().tolist())
print("   contains '@' (na=False):", users["email"].str.contains("@", na=False).tolist())

# ─── 5. pivot: из длинной в широкую ────────────────────────────
print("\n5) PIVOT: ДЛИННАЯ ФОРМА → ШИРОКАЯ")
long = pd.DataFrame(
    {
        "user": ["anna", "anna", "ivan", "ivan"],
        "quarter": ["Q1", "Q2", "Q1", "Q2"],
        "amount": [100, 200, 300, 400],
    }
)
print("   long:\n", long)
wide = long.pivot(index="user", columns="quarter", values="amount")
print("   wide:\n", wide)

# ─── 6. melt: обратно в длинную ────────────────────────────────
print("\n6) MELT: ШИРОКАЯ ФОРМА → ДЛИННАЯ")
back = wide.reset_index().melt(id_vars="user", var_name="quarter", value_name="amount")
print(back)

# ─── 7. explode: список в строки ───────────────────────────────
print("\n7) EXPLODE: СПИСОК ТОВАРОВ В ОТДЕЛЬНЫЕ СТРОКИ")
baskets = pd.DataFrame(
    {"order_id": [1, 2], "items": [["apple", "pear"], ["bread"]]}
)
print(baskets)
print(baskets.explode("items"))

# ─── 8. pivot_table с агрегацией ───────────────────────────────
print("\n8) PIVOT_TABLE: ЕСЛИ В ЯЧЕЙКЕ НЕСКОЛЬКО ЗНАЧЕНИЙ")
multi = pd.DataFrame(
    {
        "user": ["anna", "anna", "ivan"],
        "quarter": ["Q1", "Q1", "Q2"],
        "amount": [100, 50, 300],
    }
)
print(multi.pivot_table(index="user", columns="quarter", values="amount", aggfunc="sum"))
print("=" * 64)
