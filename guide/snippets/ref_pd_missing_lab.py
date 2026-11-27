"""Справочник pandas: пропуски. Все примеры страницы ref-pd-missing.html.

Требуется pandas 3.0.1 (как в книге).
Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_pd_missing_lab.py

Вывод детерминирован: нет времени, id() и порядка из хеш-таблиц.
DataFrame маленькие (4 строки) и печатаются целиком, поэтому вывод
не зависит от ширины терминала и не обрезается.
"""

# ── 03. Подготовка: как выглядят пропуски ──────────────────────────────────
print("── 03. Подготовка ──")
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", None, "Москва", "Казань"],
})
print(df)
print(df.dtypes)
print(df.isna().sum())
print(df.convert_dtypes().dtypes)

# ── 05.1. Три вида пропусков ───────────────────────────────────────────────
print("\n── 05.1. Три вида пропусков ──")
for value in (np.nan, None, pd.NA):
    print(repr(value), type(value).__name__, pd.isna(value))

# ── 05.2. isna и count против size ─────────────────────────────────────────
print("\n── 05.2. isna и count ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", None, "Москва", "Казань"],
})
print(df.isna().sum())
print(len(df), df.count().tolist())
print(df.isna().any().tolist())

# ── 05.3. dropna: any, subset, thresh ──────────────────────────────────────
print("\n── 05.3. dropna ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", "Казань", None, "Казань"],
})
print(df.dropna())
print(df.dropna(subset=["amount"]))
print(df.dropna(thresh=2))

# ── 05.4. fillna, ffill, interpolate ───────────────────────────────────────
print("\n── 05.4. fillna ──")
ts = pd.DataFrame({
    "day": [1, 2, 3, 4, 5],
    "amount": [1200.0, np.nan, np.nan, 900.0, np.nan],
})
print(ts["amount"].fillna(ts["amount"].mean()).tolist())
print(ts["amount"].ffill(limit=1).tolist())
print(ts["amount"].bfill().tolist())
print(ts["amount"].interpolate().tolist())
print(ts["amount"].fillna(0).dtype)

# ── 05.5. Nullable-типы ────────────────────────────────────────────────────
print("\n── 05.5. Nullable-типы ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", None, "Москва", "Казань"],
})
amount_int = df["amount"].astype("Int64")
print(amount_int.dtype, amount_int.tolist())
print(amount_int.isna().tolist())
print(df["amount"].fillna(0).dtype)
print(df.convert_dtypes().to_string())

# ── 05.6. NaN в сравнениях и ключах ────────────────────────────────────────
print("\n── 05.6. NaN в сравнениях и ключах ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", None, "Москва", "Казань"],
})
print((df["amount"] > 500).tolist())
print((df["amount"] == np.nan).tolist())
print(df.groupby("city").size().to_dict())
print(df.groupby("city", dropna=False).size().to_dict())
print(df.sort_values("amount")["user"].tolist())

left = pd.DataFrame({"city": ["Москва", np.nan], "orders": [2, 1]})
right = pd.DataFrame({"city": [np.nan, np.nan, "Москва"], "manager": ["A", "B", "C"]})
merged = left.merge(right, on="city", how="inner")
print(merged)
print(len(left), len(merged))

# ── 06.1. Сценарий: чистка CSV ─────────────────────────────────────────────
print("\n── 06.1. Сценарий: чистка CSV ──")
df = pd.DataFrame({
    "user": ["anna", None, "olga", "petr"],
    "amount": [1200.0, 800.0, np.nan, 500.0],
    "city": ["Москва", None, "Москва", "Казань"],
})
clean = df.dropna(subset=["user"])
clean["city"] = clean["city"].fillna("неизвестно")
clean["amount_missing"] = clean["amount"].isna()
print(clean.to_string(index=False))
print(len(df), len(clean))

# ── 06.2. Сценарий: среднее по группе ──────────────────────────────────────
print("\n── 06.2. Сценарий: среднее по группе ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "city": ["Москва", "Москва", "Казань", "Казань"],
    "amount": [1200.0, np.nan, 800.0, np.nan],
})
df["amount"] = df["amount"].fillna(df.groupby("city")["amount"].transform("mean"))
print(df.to_string(index=False))

# ── 06.3. Сценарий: forward fill временного ряда ───────────────────────────
print("\n── 06.3. Сценарий: forward fill ──")
ts = pd.DataFrame({
    "date": ["2024-01-03", "2024-01-01", "2024-01-02", "2024-01-04"],
    "amount": [300.0, 1200.0, np.nan, np.nan],
})
ts["date"] = pd.to_datetime(ts["date"])
ts = ts.sort_values("date").reset_index(drop=True)
print(ts["date"].dt.day.tolist())
print(ts["amount"].tolist())
print(ts["amount"].ffill().tolist())

# ── 07. Проверка ошибок ────────────────────────────────────────────────────
print("\n── 07. Проверка ошибок ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", None, "Москва", "Казань"],
})
print("fillna(0):", df["amount"].fillna(0).dtype)
print("pd.NA == pd.NA:", repr(pd.NA == pd.NA))
print("== np.nan:", (df["amount"] == np.nan).tolist())

left = pd.DataFrame({"city": ["Москва", np.nan], "orders": [2, 1]})
right = pd.DataFrame({"city": [np.nan, np.nan, "Москва"], "manager": ["A", "B", "C"]})
print("merge NaN-ключей:", len(left.merge(right, on="city", how="inner")))

df.fillna(0)
print("fillna без присваивания, пропусков:", int(df["amount"].isna().sum()))

try:
    df.fillna(method="ffill")
except TypeError as e:
    print(type(e).__name__, e)

# ── 08a. Задача: портрет пропусков ─────────────────────────────────────────
print("\n── 08a. Задача: портрет пропусков ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
    "city": ["Москва", None, "Москва", "Казань"],
})
print(df.isna().sum().to_dict())
print((df.isna().mean() * 100).round(1).tolist())

# ── 08b. Задача: медиана и флаг ────────────────────────────────────────────
print("\n── 08b. Задача: медиана и флаг ──")
df = pd.DataFrame({
    "user": ["anna", "ivan", "olga", "petr"],
    "amount": [1200.0, np.nan, 500.0, np.nan],
})
missing = df["amount"].isna()
df["amount"] = df["amount"].fillna(df["amount"].median())
print(missing.tolist())
print(df["amount"].tolist())
