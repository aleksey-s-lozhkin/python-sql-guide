# -*- coding: utf-8 -*-
"""Справочник: дата и время в pandas. Все примеры страницы ref-dt-pandas.html.

Требуется pandas 3.0.1 (как в книге).
Запуск из корня проекта:
    python3 guide/snippets/ref_dt_pandas_lab.py

Вывод детерминирован: фиксированные даты, без now() и random.
"""

import pandas as pd


def block(title):
    """Маркер раздела — как в остальных лабораториях книги."""
    print(f"\n── {title} ──")


# ── 03. Как создать ────────────────────────────────────────────────────────
block("03. Как создать")
ts = pd.Timestamp("2024-02-01")
d = pd.to_datetime(pd.Series(["2024-01-15", "2024-02-01", "2024-03-10"]))
print(ts)
print(d.dtype)
print(d.dt.strftime("%Y-%m-%d").tolist())


# ── 05.1 Timestamp и части даты ────────────────────────────────────────────
block("05.1 Timestamp и части даты")
ts = pd.Timestamp("2024-02-01")
print(ts.year, ts.month, ts.day)
print(ts.day_name(), ts.quarter)

d = pd.to_datetime(pd.Series(["2024-01-15", "2024-02-01", "2024-03-10"]))
print(d.dt.year.tolist())
print(d.dt.month.tolist())
print(d.dt.day_name().tolist())
print(d.dt.quarter.tolist())
print(d.dt.day_of_week.tolist())
print(d.dt.isocalendar().week.tolist())


# ── 05.2 Округление и форматирование ───────────────────────────────────────
block("05.2 Округление и форматирование")
ts = pd.Timestamp("2024-02-01 13:47:05")
print(ts.floor("h"))
print(ts.ceil("h"))
print(ts.round("h"))
print(ts.normalize())

d = pd.to_datetime(pd.Series(["2024-01-15 09:20", "2024-02-01 18:05"]))
print(d.dt.floor("D").astype(str).tolist())
print(d.dt.strftime("%d.%m.%Y %H:%M").tolist())


# ── 05.3 to_datetime: формат, ошибки, UTC ─────────────────────────────────
block("05.3 to_datetime: формат, ошибки, UTC")
raw = ["15.01.2024", "02.02.2024", "01.03.2024"]
print(sorted(raw))
dates = pd.to_datetime(pd.Series(raw), format="%d.%m.%Y")
print(sorted(dates.dt.strftime("%Y-%m-%d").tolist()))

coerced = pd.to_datetime(pd.Series(["01.02.2024", "not-a-date"]),
                         format="%d.%m.%Y", errors="coerce")
print(coerced.isna().tolist())
print(coerced.iloc[0])

try:
    pd.to_datetime(pd.Series(["01.02.2024", "not-a-date"]), format="%d.%m.%Y")
except ValueError as e:
    print(type(e).__name__, str(e).split(" You might")[0])

utc = pd.to_datetime(pd.Series(["2024-01-15 10:00"]), utc=True)
print(utc.astype(str).tolist())
print(utc.dtype)


# ── 05.4 Таймзоны и DST ────────────────────────────────────────────────────
block("05.4 Таймзоны и DST")
ts = pd.Timestamp("2024-03-10 12:00:00")
print(ts.tz)
moscow = ts.tz_localize("Europe/Moscow")
print(moscow)
print(moscow.tz_convert("UTC"))
print(moscow.tz_convert("UTC").tz)

aware = pd.Series(pd.to_datetime(["2024-01-15"], utc=True))
try:
    aware > pd.Timestamp("2024-02-01")
except TypeError as e:
    print(type(e).__name__, str(e))

try:
    moscow.tz_localize("UTC")
except TypeError as e:
    print(type(e).__name__, str(e))

try:
    pd.Timestamp("2024-03-31 02:30").tz_localize("Europe/Berlin")
except ValueError as e:
    print(type(e).__name__, str(e).split(" due to")[0])

print(pd.Timestamp("2024-10-27 02:30").tz_localize("Europe/Berlin", ambiguous="NaT"))
print(pd.Timestamp("2024-03-31 02:30").tz_localize(
    "Europe/Berlin", nonexistent="shift_forward"))


# ── 05.5 Периоды, resample и арифметика ───────────────────────────────────
block("05.5 Периоды, resample и арифметика")
orders = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10", "2024-03-01"]),
    "amount": [1200, 800, 1500, 500],
})
print(orders.resample("ME", on="date")["amount"].sum())
print(orders["date"].dt.to_period("M").astype(str).tolist())
print(orders["date"].dt.to_period("M").dtype)
print(pd.period_range("2024-01", periods=3, freq="M").astype(str).tolist())
print(pd.date_range("2024-01-01", periods=3, freq="D").strftime("%Y-%m-%d").tolist())

d0 = pd.Timestamp("2024-01-05")
print(d0 + pd.Timedelta(days=10))
print(pd.Timestamp("2024-03-01") - d0)
print((d0 + pd.Timedelta("36h")))

dates = pd.to_datetime(pd.Series(["2024-01-01", "2024-01-15", "2024-02-01"]))
print(dates.between("2024-01-01", "2024-02-01").tolist())
print(((dates >= "2024-01-01") & (dates < "2024-02-01")).tolist())
print(pd.NaT, pd.isna(pd.NaT), pd.NaT == pd.NaT)


# ── 06.1 Сценарий: месячная выручка ────────────────────────────────────────
block("06.1 Сценарий: месячная выручка")
orders = pd.DataFrame({
    "user": ["Anna", "Olga", "Ivan", "Anna"],
    "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10", "2024-03-01"]),
    "amount": [1200, 800, 1500, 500],
})
monthly = orders.groupby(orders["date"].dt.to_period("M"))["amount"].sum()
print(monthly)
print(monthly.sum())


# ── 06.2 Сценарий: конвертация в зону ──────────────────────────────────────
block("06.2 Сценарий: конвертация в зону")
sent = pd.to_datetime(["2024-01-15 10:00", "2024-06-15 10:00"], utc=True)
local = sent.tz_convert("Europe/Moscow")
print(sent.astype(str).tolist())
print(local.astype(str).tolist())


# ── 06.3 Сценарий: скользящее окно по дням ─────────────────────────────────
block("06.3 Сценарий: скользящее окно по дням")
days = pd.date_range("2024-01-01", periods=8, freq="D")
revenue = pd.Series([100, 120, 80, 150, 130, 90, 110, 140], index=days)
window = revenue.rolling(3).sum().dropna()
print(window.astype(int).tolist())
print(window.index[-1].strftime("%Y-%m-%d"))


# ── 08.1 Решение: месячная выручка ─────────────────────────────────────────
block("08.1 Решение: месячная выручка")
orders = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10"]),
    "amount": [1200, 800, 1500],
})
print(orders.groupby(orders["date"].dt.to_period("M"))["amount"].sum())


# ── 08.2 Решение: конвертация в зону ───────────────────────────────────────
block("08.2 Решение: конвертация в зону")
sent = pd.to_datetime(["2024-01-15 10:00"], utc=True)
print(sent.tz_convert("Europe/Moscow").astype(str).tolist())
