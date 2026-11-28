"""Справочник pandas: Series и DataFrame — все примеры страницы ref-pd-series.html.

Требуется pandas 3.0.1 (как в книге).
Запуск из корня проекта:
    python guide/snippets/ref_pd_series_lab.py
"""
import io
import warnings

import pandas as pd

# фиксируем ширину вывода: .out на странице не должен зависеть от терминала
pd.options.display.width = 80
pd.options.display.max_columns = 20
warnings.filterwarnings("ignore", category=pd.errors.ChainedAssignmentError)

print("pandas", pd.__version__)
print("=" * 64)

# ── 03. Как создать: Series ─────────────────────────────────────────────────
print("\n── 03. Как создать: Series ──")
s = pd.Series([1200, 800, 500], index=["anna", "ivan", "olga"], name="amount")
print(s)
print(s.index.tolist(), s.dtype, s.name)
print(s.values, s.to_numpy())
print(s["anna"], s.iloc[0], s.loc["ivan"])   # метка, позиция, метка — кратко

by_dict = pd.Series({"anna": 1200, "ivan": 800, "olga": 500})
print(by_dict.index.tolist())          # порядок ключей сохранён
print(pd.Series(7, index=["a", "b", "c"]).tolist())

# ── 03. Как создать: DataFrame ──────────────────────────────────────────────
print("\n── 03. Как создать: DataFrame ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga"],
    "amount": [1200, 800, 500],
    "city": ["Москва", "Казань", "Москва"],
})
print(df)
print(df.shape, df.size, df.columns.tolist(), df.index.tolist())
print(df.dtypes)

from_rows = pd.DataFrame([
    {"user": "anna", "amount": 1200},
    {"user": "ivan", "amount": 800},
])
print(from_rows)

csv = """user,amount
anna,1200
ivan,800
"""
from_csv = pd.read_csv(io.StringIO(csv))
print(from_csv.dtypes.astype(str).tolist())

# ── 05. Series: методы ──────────────────────────────────────────────────────
print("\n── 05. Series: методы ──")
s = pd.Series({"anna": 1200, "ivan": 800, "olga": 500}, name="amount")
print(s.map(lambda v: v // 100))
print(s.apply(lambda v: v / 1000).tolist())
print(s.sort_values())
cities = pd.Series(["Москва", "Казань", "Москва", "Москва"], name="city")
print(cities.value_counts())
with_gap = pd.Series([1200, None, 500], name="amount")
print(with_gap.isna().tolist(), int(with_gap.isna().sum()))
print(s.astype("float64").dtype, s.astype(str).tolist())

# ── 05. DataFrame: свойства ─────────────────────────────────────────────────
print("\n── 05. DataFrame: свойства ──")
print(df.shape, df.size)
print(df.columns.tolist(), df.index.tolist())
print(df.dtypes)
print(df.head(2))
print(df.tail(2))
print(df.T)
print(df.memory_usage(deep=True, index=False))

# ── 05. Колонки: Series, assign, rename, drop ───────────────────────────────
print("\n── 05. Колонки: Series, assign, rename, drop ──")
print(type(df["amount"]).__name__, df["amount"].shape)
print(type(df[["user", "amount"]]).__name__, df[["user", "amount"]].shape)
print(df[["user", "amount"]])
df["amount_with_tax"] = df["amount"] * 1.2
print(df[["user", "amount", "amount_with_tax"]])
print(df.assign(amount_k=df["amount"] / 1000).columns.tolist())
print(df.rename(columns={"user": "name"}).columns.tolist())
print(df.drop(columns=["city"]).columns.tolist())
print(df["amount"].astype(str).tolist())
print(df.columns.tolist())       # исходник не изменился

# ── 05. Copy-on-Write ───────────────────────────────────────────────────────
print("\n── 05. Copy-on-Write ──")
df = pd.DataFrame({"user": ["anna", "ivan"], "amount": [1200, 800]})
df["amount"][0] = 999            # так делать нельзя: в pandas 3 только предупредит
print(df["amount"].tolist())     # [1200, 800] — исходник не изменился
df2 = df.copy()                  # CoW: независимая копия
df2["amount"] = df2["amount"] * 2
print(df["amount"].tolist(), df2["amount"].tolist())
col = df["amount"]
df["amount"] = [1500, 900]
print(col.tolist())              # [1200, 800] — колонка не «увидела» правку
s1 = pd.Series([1200, 800], index=["anna", "ivan"])
s2 = pd.Series([100, 50], index=["ivan", "olga"])
print(s1 + s2)

# ── 05. NaN и dtype ─────────────────────────────────────────────────────────
print("\n── 05. NaN и dtype ──")
df = pd.DataFrame({"amount": [1200, None, 500]})
print(df)
print(df["amount"].dtype)                       # float64: NaN не влез в int64
print(df["amount"].astype("Int64").tolist())    # nullable: пропуск остаётся <NA>

# ── 06. Сценарий: заказы ────────────────────────────────────────────────────
print("\n── 06. Сценарий: заказы ──")
orders = pd.DataFrame([
    {"user": "anna", "amount": 1200},
    {"user": "ivan", "amount": 800},
    {"user": "olga", "amount": 500},
])
orders["amount_with_tax"] = orders["amount"] * 1.2
top = orders.sort_values("amount", ascending=False).head(2)
print(top)

# ── 06. Сценарий: CSV ───────────────────────────────────────────────────────
print("\n── 06. Сценарий: CSV ──")
csv = """user,amount,city
anna,1200,Москва
ivan,800,Казань
olga,500,Москва
"""
df2 = pd.read_csv(io.StringIO(csv))
print(df2.shape, df2.size)
print(df2.head(2))

# ── 06. Сценарий: первый обзор ──────────────────────────────────────────────
print("\n── 06. Сценарий: первый обзор ──")
df2.info(verbose=False)
print(df2.describe())

# ── 08. Задача 01: надбавка 10% ─────────────────────────────────────────────
print("\n── 08. Задача 01: надбавка 10% ──")
amounts = pd.Series({"anna": 1200, "ivan": 800, "olga": 500})
bonus = amounts.map(lambda v: v * 1.1)
print(bonus.sort_values(ascending=False).round(1))

# ── 08. Задача 02: name и total ─────────────────────────────────────────────
print("\n── 08. Задача 02: name и total ──")
orders = pd.DataFrame([
    {"user": "anna", "amount": 1200, "qty": 2},
    {"user": "ivan", "amount": 800, "qty": 1},
])
orders["total"] = orders["amount"] * orders["qty"]
report = orders[["user", "total"]].rename(columns={"user": "name"})
print(report)
