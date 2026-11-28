# -*- coding: utf-8 -*-
"""Справочник pandas: loc и iloc. Все примеры страницы ref-pd-loc.html.

Требуется pandas 3.0.1 (как в книге).

Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_pd_loc_lab.py

Вывод детерминирован: порядок строк задан явно, таблицы печатаются целиком,
без времени, случайных чисел и хешей. Каждый блок ниже — отдельный фрагмент
страницы; блоки не зависят от предыдущих, а всё, что меняется, меняется
на копии `df`, поэтому вывод блока совпадает с выводом всей лаборатории.
"""
import pandas as pd

pd.set_option("display.width", 80)

df = pd.DataFrame(
    {"amount": [1200, 800, 500], "city": ["Москва", "Казань", "Москва"]},
    index=["anna", "ivan", "olga"],
)
orders = pd.DataFrame(
    {"user": ["anna", "ivan", "olga"], "amount": [1200, 800, 500]},
    index=["A-101", "A-102", "A-103"],
)
big = pd.DataFrame({"id": range(100, 125), "amount": range(25)})


# ── БЛОК 03 · Подготовка: DataFrame и индекс ────────────────────────────
frame = pd.DataFrame({"amount": [1200, 800], "city": ["Москва", "Казань"]})
print(frame)
print(type(frame.index).__name__, frame.index.tolist())

named = frame.set_index("city")
print(named)
print(named.index.tolist())

back = named.reset_index()
print(back)
print(type(back.index).__name__)


# ── БЛОК 05a · Одна таблица, два способа ────────────────────────────────
print(df.loc["ivan", "amount"])   # подпись строки и имя колонки
print(df.iloc[1, 0])              # номер строки и номер колонки

odd = pd.DataFrame({"v": [10, 20, 30]}, index=[10, 20, 30])
print(odd.loc[30].tolist())       # строка с меткой 30
print(odd.iloc[1].tolist())       # вторая строка по счёту


# ── БЛОК 05b · Срезы: разная граница ────────────────────────────────────
print(df.loc["anna":"olga"])      # правая метка включена
print(df.iloc[0:2])               # правая позиция не включена


# ── БЛОК 05c · Строки и колонки вместе ──────────────────────────────────
print(df.columns.tolist(), df.index.tolist())
print(df.loc[:, "city"].tolist())
print(df.loc[["anna", "olga"], ["amount"]])
print(df.iloc[[0, 2], [0]])


# ── БЛОК 05d · Маска внутри loc ─────────────────────────────────────────
print(df.loc[df["amount"] > 600, ["city", "amount"]])


# ── БЛОК 05g · Дубли индекса меняют тип ─────────────────────────────────
dup = pd.DataFrame({"x": [1, 2]}, index=["a", "a"])
print(dup.loc["a"])
print(type(dup.loc["a"]).__name__, dup.index.is_unique)


# ── БЛОК 05h · Запись: маска и метка ────────────────────────────────────
d = df.copy()
d.loc[d["amount"] > 1000, "flag"] = True
d.loc["ivan", "amount"] = 850
print(d.to_string())


# ── БЛОК 05i · Цепочка присваиваний не пишет ────────────────────────────
d = df.copy()
d[d["amount"] > 1000]["amount"] = 0   # ChainedAssignmentError в stderr — так и должно быть
print(d.to_string())


# ── БЛОК 05j · Новая метка расширяет таблицу ────────────────────────────
d = df.copy()
d.loc["petr"] = {"amount": 700, "city": "Тверь"}
d.loc["maria", "amount"] = 450
print(d.to_string())
print(d["amount"].dtype, d.index.tolist())


# ── БЛОК 06a · Сценарий: заказ по id ────────────────────────────────────
print(orders.loc["A-102"].to_string())
print(orders.loc["A-102", "amount"])


# ── БЛОК 06b · Сценарий: срез строк 10–20 ───────────────────────────────
print(big.loc[10:20, "id"].tolist())
print(big.iloc[10:21, 0].tolist())
print(len(big.loc[10:20]), len(big.iloc[10:21]))


# ── БЛОК 06c · Сценарий: флаг дорогим заказам ───────────────────────────
d = df.copy()
d["vip"] = False
d.loc[d["amount"] > 1000, "vip"] = True
print(d.to_string())
