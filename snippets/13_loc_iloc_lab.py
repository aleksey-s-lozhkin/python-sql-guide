"""Лаборатория к главе 13: loc и iloc.

Запуск:  python3 guide/snippets/13_loc_iloc_lab.py
"""
import pandas as pd

print("pandas", pd.__version__)
print("=" * 64)

df = pd.DataFrame(
    {"amount": [1200, 800, 500], "city": ["Москва", "Казань", "Москва"]},
    index=["anna", "ivan", "olga"],
)
print("df:\n", df)

# ─── 1. loc по метке ─────────────────────────────────────────────
print("\n1) LOC — ПО МЕТКЕ ИНДЕКСА")
print("   df.loc['ivan']:\n", df.loc["ivan"])
print("   df.loc['ivan', 'amount']:", df.loc["ivan", "amount"])

# ─── 2. iloc по позиции ──────────────────────────────────────────
print("\n2) ILOC — ПО ПОЗИЦИИ")
print("   df.iloc[1]:\n", df.iloc[1])
print("   df.iloc[1, 0]:", df.iloc[1, 0])

# ─── 3. Срезы: включительно против исключительно ─────────────────
print("\n3) СРЕЗЫ: LOC ВКЛЮЧАЕТ ГРАНИЦУ, ILOC — НЕТ")
print("   df.loc['anna':'ivan']:\n", df.loc["anna":"ivan"])
print("   df.iloc[0:2]:\n", df.iloc[0:2])

# ─── 4. Строки и столбцы вместе ──────────────────────────────────
print("\n4) СТРОКИ И СТОЛБЦЫ ВМЕСТЕ")
print("   df.loc[['anna', 'olga'], ['amount']]:\n", df.loc[["anna", "olga"], ["amount"]])
print("   df.iloc[[0, 2], [0]]:\n", df.iloc[[0, 2], [0]])
print("   df.iloc[:, 1]:", df.iloc[:, 1].tolist())

# ─── 5. Маска и loc ──────────────────────────────────────────────
print("\n5) МАСКА + LOC")
print(df.loc[df["amount"] > 600, ["city", "amount"]])

# ─── 6. at и iat: скаляр без Series ──────────────────────────────
print("\n6) AT И IAT — ДОСТУП К ОДНОМУ ЗНАЧЕНИЮ")
print("   df.at['ivan', 'amount']:", df.at["ivan", "amount"])
print("   df.iat[1, 0]:", df.iat[1, 0])

# ─── 7. Метка и позиция расходятся ───────────────────────────────
print("\n7) КОГДА МЕТКА И ПОЗИЦИЯ РАСХОДЯТСЯ")
odd = pd.DataFrame({"v": [10, 20, 30]}, index=[10, 20, 30])
print(odd)
print("   odd.loc[30]  → строка с меткой 30:", odd.loc[30].tolist())
print("   odd.iloc[1]  → вторая строка      :", odd.iloc[1].tolist())

# ─── 8. Дубли индекса ────────────────────────────────────────────
print("\n8) ДУБЛИ ИНДЕКСА")
dup = pd.DataFrame({"x": [1, 2]}, index=["a", "a"])
print(dup)
print("   dup.loc['a']:\n", dup.loc["a"])

# ─── 9. Присваивание через loc ───────────────────────────────────
print("\n9) ЗАПИСЬ ТОЛЬКО ЧЕРЕЗ .LOC")
df.loc["ivan", "amount"] = 850
print(df)
print("   df[df['city'] == 'Москва'].shape:", df[df["city"] == "Москва"].shape)
print("=" * 64)
