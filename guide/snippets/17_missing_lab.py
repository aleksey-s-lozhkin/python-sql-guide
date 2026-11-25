"""Лаборатория к главе 17: пропуски.

Запуск:  python3 guide/snippets/17_missing_lab.py
"""
import numpy as np
import pandas as pd

print("pandas", pd.__version__)
print("=" * 64)

df = pd.DataFrame(
    {
        "user": ["anna", "ivan", "olga", "petr"],
        "amount": [1200, np.nan, 500, np.nan],
        "city": ["Москва", None, "Москва", "Казань"],
    }
)
print("df:\n", df)
print("dtypes:\n", df.dtypes)

# ─── 1. Три вида отсутствия ─────────────────────────────────────
print("\n1) ЧЕМ ПРЕДСТАВЛЕНЫ ПРОПУСКИ")
print("   np.nan :", repr(np.nan), "| тип:", type(np.nan).__name__)
print("   None   :", repr(None), "| тип:", type(None).__name__)
print("   pd.NA  :", repr(pd.NA), "| тип:", type(pd.NA).__name__)

# ─── 2. isna и notna ────────────────────────────────────────────
print("\n2) ISNA И NOTNA")
print("   isna:\n", df.isna())
print("   сумма по колонкам:\n", df.isna().sum())

# ─── 3. count против size ───────────────────────────────────────
print("\n3) COUNT СЧИТАЕТ НЕПУСТЫЕ, SIZE — ВСЕ")
print("   len(df):", len(df))
print("   df.count():\n", df.count())

# ─── 4. dropna ──────────────────────────────────────────────────
print("\n4) DROPNA: УДАЛИТЬ")
print("   dropna():\n", df.dropna())
print("   dropna(subset=['amount']):\n", df.dropna(subset=["amount"]))

# ─── 5. fillna ──────────────────────────────────────────────────
print("\n5) FILLNA: ЗАПОЛНИТЬ")
print("   средним:\n", df["amount"].fillna(df["amount"].mean()))
print("   нулём:\n", df["amount"].fillna(0))
print("   dtypes после fillna(0):\n", df["amount"].fillna(0).dtypes)

# ─── 6. ffill и bfill ──────────────────────────────────────────
print("\n6) FFILL И BFILL")
print("   amount.ffill():\n", df["amount"].ffill())
print("   amount.bfill():\n", df["amount"].bfill())

# ─── 7. Nullable-типы: Int64 вместо float ──────────────────────
print("\n7) NULLABLE-ТИПЫ: Int64 ВМЕСТО FLOAT64")
amount_int = df["amount"].astype("Int64")
print("   dtype:", amount_int.dtype, "| значения:", amount_int.tolist())
print("   isna:", amount_int.isna().tolist())

# ─── 8. Пропуск как индикатор ──────────────────────────────────
print("\n8) ПРОПУСК КАК ПРИЗНАК")
df["amount_missing"] = df["amount"].isna()
print(df[["user", "amount", "amount_missing"]])

# ─── 9. groupby и NaN в ключе ──────────────────────────────────
print("\n9) GROUPBY: ЧТО ПРОИСХОДИТ С NaN В КЛЮЧЕ")
print("   по умолчанию:\n", df.groupby("city").size())
print("   dropna=False:\n", df.groupby("city", dropna=False).size())
print("=" * 64)
