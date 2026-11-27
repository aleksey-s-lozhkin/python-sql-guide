"""Справочник pandas: даты и reshape. Все примеры страницы ref-pd-reshape.html.

Требуется pandas 3.0.1 (как в книге).
Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_pd_reshape_lab.py

Вывод детерминирован: нет времени, id() и порядка из хеш-таблиц,
сортировки заданы явно. Таблицы маленькие и печатаются целиком.
"""

# ── 03. Подготовка: длинная таблица и «грязный» CSV ────────────────────────
print("── 03. Подготовка ──")
import pandas as pd

long = pd.DataFrame({
    "user": ["anna", "anna", "ivan", "ivan"],
    "quarter": ["Q1", "Q2", "Q1", "Q2"],
    "amount": [100, 200, 300, 400],
})
raw = pd.DataFrame({
    "user": ["  Anna ", "Ivan", "Olga"],
    "email": [" Anna@Mail.RU ", "ivan@corp.io", "olga@mail.ru"],
    "date": ["2024-01-05", "2024-02-11", "2024-03-02"],
})
print(long.to_string(index=False))
print(raw.to_string(index=False))
print(long.dtypes.astype(str).tolist())

# ── 05.1. pivot: длинная → широкая ─────────────────────────────────────────
print("\n── 05.1. pivot ──")
wide = long.pivot(index="user", columns="quarter", values="amount")
print(wide)
print(wide.columns.tolist())

# ── 05.2. pivot на дублях и pivot_table ────────────────────────────────────
print("\n── 05.2. pivot на дублях ──")
dup = pd.DataFrame({
    "user": ["anna", "anna", "ivan"],
    "quarter": ["Q1", "Q1", "Q2"],
    "amount": [100, 150, 300],
})
try:
    dup.pivot(index="user", columns="quarter", values="amount")
except ValueError as e:
    print(type(e).__name__, e)
print(dup.pivot_table(index="user", columns="quarter", values="amount", aggfunc="sum"))

# ── 05.3. melt: широкая → длинная ──────────────────────────────────────────
print("\n── 05.3. melt ──")
back = wide.reset_index().melt(id_vars="user", var_name="quarter", value_name="amount")
print(back.to_string(index=False))
print(len(wide), len(back))

# ── 05.4. explode: список → строки ─────────────────────────────────────────
print("\n── 05.4. explode ──")
baskets = pd.DataFrame({
    "order_id": [1, 2, 3],
    "items": [["apple", "pear"], ["bread"], []],
})
print(baskets.explode("items").to_string(index=False))
scalar = pd.DataFrame({"order_id": [1, 2], "items": ["apple", "bread"]})
print(scalar.explode("items").to_string(index=False))
print(len(scalar), len(scalar.explode("items")))

# ── 05.5. crosstab и concat ────────────────────────────────────────────────
print("\n── 05.5. crosstab и concat ──")
events = pd.DataFrame({
    "user": ["anna", "anna", "ivan", "olga"],
    "status": ["paid", "paid", "new", "paid"],
})
print(pd.crosstab(events["user"], events["status"]))
jan = pd.DataFrame({"user": ["anna"], "amount": [100]})
feb = pd.DataFrame({"user": ["ivan"], "amount": [300]})
print(pd.concat([jan, feb], ignore_index=True).to_string(index=False))

# ── 05.6. Аксессор .dt ─────────────────────────────────────────────────────
print("\n── 05.6. .dt ──")
orders = pd.DataFrame({
    "date": ["2024-01-05", "2024-02-11", "2024-03-02"],
    "amount": [100, 300, 400],
})
orders["date"] = pd.to_datetime(orders["date"])
print(orders["date"].dtype)
print(orders["date"].dt.year.tolist(), orders["date"].dt.month.tolist())
print(orders["date"].dt.day.tolist())
print(orders["date"].dt.strftime("%d.%m.%Y").tolist())
orders["month"] = orders["date"].dt.to_period("M")
print(orders.groupby("month")["amount"].sum())

# ── 05.7. Аксессор .str ────────────────────────────────────────────────────
print("\n── 05.7. .str ──")
clean = pd.DataFrame({
    "user": ["  Anna ", "Ivan", "Olga"],
    "email": [" Anna@Mail.RU ", "ivan@corp.io", "olga@mail.ru"],
})
clean["email"] = clean["email"].str.strip().str.lower()
clean["user"] = clean["user"].str.strip().str.lower()
clean["domain"] = clean["email"].str.extract(r"@([\w.]+)$", expand=False)
clean["has_at"] = clean["email"].str.contains("@", regex=False)
print(clean.to_string(index=False))
print(clean["email"].str.len().tolist())
print(clean["email"].str.split("@", expand=True))

# ── 06.1. Сценарий: месячная сводка ────────────────────────────────────────
print("\n── 06.1. Сценарий: месячная сводка ──")
orders = pd.DataFrame({
    "date": ["2024-01-05", "2024-01-20", "2024-02-11", "2024-03-02"],
    "amount": [100, 200, 300, 400],
})
orders["date"] = pd.to_datetime(orders["date"])
monthly = orders.groupby(orders["date"].dt.to_period("M"))["amount"].sum()
print(monthly)

# ── 06.2. Сценарий: wide → long ────────────────────────────────────────────
print("\n── 06.2. Сценарий: wide → long ──")
wide2 = pd.DataFrame({
    "user": ["anna", "ivan"],
    "Q1": [100, 300],
    "Q2": [200, 400],
})
long2 = wide2.melt(id_vars="user", var_name="quarter", value_name="amount")
print(long2.sort_values(["user", "quarter"]).to_string(index=False))

# ── 06.3. Сценарий: разбор дат и email-домена ──────────────────────────────
print("\n── 06.3. Сценарий: даты и email ──")
raw = pd.DataFrame({
    "user": ["  Anna ", "Ivan", "Olga"],
    "email": [" Anna@Mail.RU ", "ivan@corp.io", "olga@mail.ru"],
    "date": ["2024-01-05", "2024-02-11", "2024-03-02"],
})
raw["user"] = raw["user"].str.strip().str.lower()
raw["email"] = raw["email"].str.strip().str.lower()
raw["domain"] = raw["email"].str.extract(r"@([\w.]+)$", expand=False)
raw["year"] = pd.to_datetime(raw["date"]).dt.year
print(raw.sort_values("user").to_string(index=False))

# ── 07. Проверка ошибок ────────────────────────────────────────────────────
print("\n── 07. Проверка ошибок ──")
dup = pd.DataFrame({
    "user": ["anna", "anna", "ivan"],
    "quarter": ["Q1", "Q1", "Q2"],
    "amount": [100, 150, 300],
})
try:
    dup.pivot(index="user", columns="quarter", values="amount")
except ValueError as e:
    print(type(e).__name__, e)
try:
    pd.Series([1200.0, 500.0]).str.lower()
except AttributeError as e:
    print(type(e).__name__, e)
try:
    pd.Series(["2024-01-05"]).dt.year
except AttributeError as e:
    print(type(e).__name__, e)
try:
    pd.to_datetime(pd.Series(["2024-01-05", "05.02.2024"]))
except ValueError as e:
    print(type(e).__name__, str(e).splitlines()[0])
scalar = pd.DataFrame({"order_id": [1, 2], "items": ["apple", "bread"]})
print("explode скаляра:", len(scalar), "→", len(scalar.explode("items")))

# ── 08a. Задача: месяцы в колонки ──────────────────────────────────────────
print("\n── 08a. Задача: месяцы в колонки ──")
orders = pd.DataFrame({
    "user": ["anna", "anna", "ivan", "anna"],
    "date": ["2024-01-05", "2024-02-11", "2024-01-20", "2024-03-02"],
    "amount": [100, 300, 200, 400],
})
orders["month"] = pd.to_datetime(orders["date"]).dt.strftime("%Y-%m")
print(pd.crosstab(orders["user"], orders["month"],
                  values=orders["amount"], aggfunc="sum"))

# ── 08b. Задача: домены из email ───────────────────────────────────────────
print("\n── 08b. Задача: домены из email ──")
users = pd.DataFrame({
    "email": [" Anna@Mail.RU ", "ivan@corp.io", "olga@mail.ru", "petr@corp.io"],
})
users["email"] = users["email"].str.strip().str.lower()
users["domain"] = users["email"].str.extract(r"@([\w.]+)$", expand=False)
print(users["domain"].value_counts().sort_index().to_dict())
