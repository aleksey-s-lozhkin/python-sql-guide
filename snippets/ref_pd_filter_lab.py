# -*- coding: utf-8 -*-
"""Справочник pandas: фильтрация. Все примеры страницы ref-pd-filter.html.

Требуется pandas 3.0.1 (как в книге).

Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_pd_filter_lab.py

Вывод детерминирован: порядок строк задан явно, таблицы печатаются целиком,
без времени, случайных чисел и хешей. В таблице специально есть пропуск
в amount. Каждый блок ниже — отдельный фрагмент страницы; всё, что меняется,
меняется на копии `df`.
"""
import numpy as np
import pandas as pd

pd.set_option("display.width", 80)

df = pd.DataFrame(
    {
        "user": ["anna", "ivan", "olga", "petr"],
        "amount": [1200.0, 800.0, 500.0, np.nan],
        "city": ["Москва", "Казань", "Москва", "Тверь"],
        "email": ["anna@mail.ru", "ivan@corp.ru", "olga@mail.ru", "petr@corp.ru"],
    }
)


# ── БЛОК 03 · Маска — такой же объект, как колонка ──────────────────────
mask = df["amount"] > 1000
print(mask)
print(type(mask).__name__, mask.dtype, len(mask))
print(df[mask].to_string())


# ── БЛОК 05a · Маска и выбор колонок ────────────────────────────────────
print(df.loc[df["amount"] > 1000, ["user", "city"]].to_string())
print(df[df["amount"] > 1000]["user"].tolist())


# ── БЛОК 05b · Логика: &, |, ~ и скобки ────────────────────────────────
both = (df["amount"] > 600) & (df["city"] == "Москва")
print(both.tolist())
print(df[both].to_string())

print(df[(df["city"] == "Казань") | (df["amount"] > 1000)]["user"].tolist())
print(df[~df["city"].isin(["Москва"])]["user"].tolist())


# ── БЛОК 05d · isin и between ───────────────────────────────────────────
print(df[df["city"].isin(["Казань", "Тверь"])]["user"].tolist())
print(df["amount"].between(800, 1200).tolist())
print(df[df["amount"].between(800, 1200)]["user"].tolist())


# ── БЛОК 05e · Текст: contains и na ─────────────────────────────────────
print(df["city"].str.contains("Мос").tolist())
print(df[df["city"].str.contains("Мос", na=False)]["user"].tolist())
print(df[df["user"].str.contains("an")]["user"].tolist())


# ── БЛОК 05f · Пропуски: isna и notna ──────────────────────────────────
print(df[df["amount"].isna()].to_string())
print(df["amount"].notna().tolist())
print(df["amount"].isna().sum())


# ── БЛОК 05g · query и filter по колонкам ───────────────────────────────
print(df.query("amount > 600 and city == 'Москва'").to_string())
limit = 600
print(df.query("amount > @limit")["user"].tolist())
print(df.filter(like="am", axis=1).columns.tolist())


# ── БЛОК 05h · Топ-N и дубли ────────────────────────────────────────────
print(df.nlargest(2, "amount")[["user", "amount"]].to_string())
print(df.sort_values("amount", ascending=False).head(2)["user"].tolist())
print(df.drop_duplicates(subset="city")["user"].tolist())


# ── БЛОК 05i · NaN в масках и арифметика ───────────────────────────────
print((df["amount"] == np.nan).tolist())
print((df["amount"] > 600).tolist())
print((df["amount"] <= 600).tolist())

mask = df["amount"] > 600
print(mask.sum(), mask.mean())
print(f"{mask.mean():.2f}")


# ── БЛОК 05k · in по колонке и isin ─────────────────────────────────────
print("anna" in df["user"])
print("anna" in df["user"].values)
print(df["user"].isin(["anna"]).tolist())


# ── БЛОК 05l · Цепочка присваиваний не пишет ────────────────────────────
d = df.copy()
d[d["amount"] > 1000]["amount"] = 0   # ChainedAssignmentError в stderr — так и должно быть
print(d["amount"].tolist())


# ── БЛОК 06a · Сценарий: дорогие заказы ─────────────────────────────────
expensive = df[df["amount"] > 600]
print(expensive[["user", "amount"]].to_string())
print(expensive["amount"].sum())


# ── БЛОК 06b · Сценарий: города из списка ───────────────────────────────
cities = ["Москва", "Тверь"]
print(df[df["city"].isin(cities)].to_string())


# ── БЛОК 06c · Сценарий: email содержит домен ───────────────────────────
print(df[df["email"].str.contains("mail.ru", regex=False)]["user"].tolist())
print(df[df["email"].str.endswith("@mail.ru")]["user"].tolist())
