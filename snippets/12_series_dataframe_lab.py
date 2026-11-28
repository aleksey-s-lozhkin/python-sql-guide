"""Лаборатория к главе 12: Series и DataFrame.

Запуск:  python3 guide/snippets/12_series_dataframe_lab.py
"""
import io

import numpy as np
import pandas as pd

print("pandas", pd.__version__, "| numpy", np.__version__)
print("=" * 64)

# ─── 1. Series: значения плюс индекс ──────────────────────────────
print("\n1) SERIES: ЗНАЧЕНИЯ ПЛЮС ИНДЕКС")
s = pd.Series([1200, 800, 500], index=["anna", "ivan", "olga"], name="amount")
print(s)
print("   index :", s.index.tolist())
print("   values:", s.values, "| dtype:", s.dtype, "| name:", s.name)

# ─── 2. DataFrame: таблица из колонок ────────────────────────────
print("\n2) DATAFRAME: ТАБЛИЦА ИЗ КОЛОНОК")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga"],
    "amount": [1200, 800, 500],
    "city": ["Москва", "Казань", "Москва"],
})
print(df)
print("   shape   :", df.shape)
print("   columns :", df.columns.tolist())
print("   index   :", df.index.tolist())
print("   dtypes  :\n", df.dtypes)

# ─── 3. Типы колонок ─────────────────────────────────────────────
print("\n3) ТИПЫ КОЛОНОК — СВОЙ У КАЖДОЙ")
print("   amount:", df["amount"].dtype)
print("   city  :", df["city"].dtype, " ← в pandas 3 строки по умолчанию str")
print("   user  :", df["user"].dtype)

# ─── 4. DataFrame — это набор Series с общим индексом ────────────
print("\n4) КОЛОНКА — ЭТО SERIES")
col = df["amount"]
print("   type(df['amount']):", type(col).__name__)
print("   col.index:", col.index.tolist())
print("   col.name :", col.name)

# ─── 5. Чтение CSV из строки ─────────────────────────────────────
print("\n5) ЧТЕНИЕ CSV (ЗДЕСЬ — ИЗ СТРОКИ, ЧТОБЫ НЕ ЗАВИСЕТЬ ОТ ФАЙЛОВ)")
csv = """user,amount,city
anna,1200,Москва
ivan,800,Казань
olga,500,Москва
"""
df2 = pd.read_csv(io.StringIO(csv))
print(df2)
print("   shape:", df2.shape, "| size:", df2.size)

# ─── 6. Первый взгляд на данные ──────────────────────────────────
print("\n6) ПЕРВЫЙ ВЗГЛЯД: HEAD, INFO, DESCRIBE")
print("   head(2):\n", df2.head(2))
print("\n   info:")
df2.info()
print("\n   describe:")
print(df2.describe())

# ─── 7. values против to_numpy ───────────────────────────────────
print("\n7) VALUES — ЭТО NUMPY-МАССИВ")
print("   type(df2.values):", type(df2.values).__name__, "| dtype:", df2.values.dtype)
print("   df2.to_numpy().shape:", df2.to_numpy().shape)

# ─── 8. Новая колонка через вычисление ───────────────────────────
print("\n8) НОВАЯ КОЛОНКА — ВЕКТОРНАЯ ОПЕРАЦИЯ")
df2["amount_with_tax"] = df2["amount"] * 1.2
print(df2[["user", "amount", "amount_with_tax"]])

# ─── 9. Индекс — не номер строки ─────────────────────────────────
print("\n9) ИНДЕКС — НЕ НОМЕР СТРОКИ")
shuffled = df2.sort_values("amount")
print(shuffled)
print("   index после сортировки:", shuffled.index.tolist())
print("   iloc[0] — первая строка РЕЗУЛЬТАТА, а не строка с меткой 0")
print("=" * 64)
