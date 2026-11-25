"""Лаборатория к главе 14: фильтрация.

Запуск:  python3 guide/snippets/14_filtering_lab.py
"""
import numpy as np
import pandas as pd

print("pandas", pd.__version__)
print("=" * 64)

df = pd.DataFrame(
    {
        "user": ["anna", "ivan", "olga", "petr"],
        "amount": [1200, 800, 500, np.nan],
        "city": ["Москва", "Казань", "Москва", "Москва"],
    }
)
print("df:\n", df)
print("dtypes:\n", df.dtypes)

# ─── 1. Маска — это Series bool ──────────────────────────────────
print("\n1) МАСКА — ЭТО SERIES BOOL, А НЕ «ФИЛЬТР ВНУТРИ»")
mask = df["amount"] > 600
print("   mask:\n", mask)
print("   type:", type(mask).__name__, "| длина:", len(mask))
print("   df[mask]:\n", df[mask])

# ─── 2. Несколько условий ────────────────────────────────────────
print("\n2) НЕСКОЛЬКО УСЛОВИЙ: & И СКОБКИ")
both = (df["amount"] > 600) & (df["city"] == "Москва")
print("   both:\n", both)
print("   df[both]:\n", df[both])

# ─── 3. isin: проверка по списку ────────────────────────────────
print("\n3) ISIN — КАК SQL IN")
print(df[df["city"].isin(["Казань", "Тверь"])])
print("   not isin (как NOT IN, но без ловушки NULL):")
print(df[~df["city"].isin(["Москва"])])

# ─── 4. between ─────────────────────────────────────────────────
print("\n4) BETWEEN — ДИАПАЗОН ВКЛЮЧИТЕЛЬНО")
print(df[df["amount"].between(600, 1200)])

# ─── 5. str.contains ────────────────────────────────────────────
print("\n5) STR.CONTAINS — ПОИСК ПО ТЕКСТУ")
print(df[df["user"].str.contains("an", case=False)])

# ─── 6. Пропуски ────────────────────────────────────────────────
print("\n6) ПРОПУСКИ: ISNA И NOTNA")
print("   isna:\n", df["amount"].isna())
print("   df[df['amount'].isna()]:\n", df[df["amount"].isna()])
print("   df[df['amount'].notna()]:\n", df[df["amount"].notna()])

# ─── 7. Маска как число ─────────────────────────────────────────
print("\n7) МАСКА — ЭТО ЕЩЁ И ЧИСЛА")
print("   mask.sum() (сколько прошло):", mask.sum())
print("   mask.mean() (доля):", round(mask.mean(), 2))

# ─── 8. loc + маска + колонки ───────────────────────────────────
print("\n8) МАСКА, LOC И ВЫБОР КОЛОНОК")
print(df.loc[df["amount"] > 600, ["user", "amount"]])

# ─── 9. query ───────────────────────────────────────────────────
print("\n9) QUERY: SQL-ПОДОБНАЯ ЗАПИСЬ")
print(df.query("amount > 600 and city == 'Москва'"))
print(df.query("city == @city", local_dict={"city": "Казань"}))
print("=" * 64)
