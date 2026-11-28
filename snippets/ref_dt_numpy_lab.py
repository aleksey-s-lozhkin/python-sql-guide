"""Справочник «Дата и время», страница 2: NumPy datetime64.

Все примеры страницы ref-dt-numpy.html.

Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_dt_numpy_lab.py

Требуется numpy 2.3.5 (как в книге). Время и now() не используются:
все даты фиксированные, вывод детерминирован.
"""

import warnings
from datetime import datetime, timedelta, timezone

import numpy as np

# ── 03.1 Как создать ───────────────────────────────────────────────────────
print("\n== 03.1 Создание ==")
import numpy as np

day = np.datetime64("2024-01-01")
print(day, day.dtype)

dates = np.array(["2024-01-01", "2024-02-15", "2024-03-10"],
                 dtype="datetime64[D]")
print(dates)
print(dates.dtype)

days = np.arange("2024-01-01", "2024-01-08", dtype="datetime64[D]")
print(days)

moment = np.datetime64("2024-03-15T10:30:45.123456789")
print(moment, moment.dtype)

# ── 05.1 Единицы и точность ────────────────────────────────────────────────
print("\n== 05.1 Единицы ==")
for unit in ["Y", "M", "W", "D", "h", "m", "s", "ms", "us", "ns"]:
    print(unit, "→", np.datetime64("2024-03-15T10:30:45.123456789", unit))

moment = np.datetime64("2024-03-15T10:30:45.123456789")
print(moment)
print(moment.astype("datetime64[D]"))
print(moment.astype("datetime64[h]"))
print(moment.astype("datetime64[s]"))
print(moment.astype("datetime64[ns]").dtype)

# ── 05.2 Диапазоны ─────────────────────────────────────────────────────────
print("\n== 05.2 Диапазоны ==")
every_two = np.arange("2024-01-01", "2024-01-11",
                      np.timedelta64(2, "D"), dtype="datetime64[D]")
print(every_two)

months = np.arange("2024-01", "2025-01", dtype="datetime64[M]")
print(months)

hours = np.arange("2024-01-01T00", "2024-01-01T06:00",
                  dtype="datetime64[h]")
print(hours)

# ── 05.3 Разности и длительности ───────────────────────────────────────────
print("\n== 05.3 Разности ==")
dates = np.array(["2024-01-01", "2024-01-10", "2024-02-01"],
                 dtype="datetime64[D]")
print(dates[1] - dates[0])
print(dates - dates[0])
print((dates - dates[0]).dtype)

print(dates + np.timedelta64(3, "D"))
print(np.timedelta64(36, "h"))
print(np.timedelta64(36, "h").astype("timedelta64[D]"))
print(np.timedelta64(3, "D") / np.timedelta64(1, "D"))
print(np.timedelta64(90, "m") / np.timedelta64(1, "h"))

early = np.datetime64("2024-02-28T09:15")
late = np.datetime64("2024-03-01T12:00")
gap = late - early
print(gap)
print(gap.astype("timedelta64[h]"))
print(dates[0].astype(int))
print(np.datetime64("2024-01-01T00:00:00").astype(int))

# ── 05.4 NaT и сравнения ───────────────────────────────────────────────────
print("\n== 05.4 NaT ==")
mixed = np.array(["2024-01-01", "NaT", "2024-03-01"],
                 dtype="datetime64[D]")
print(mixed)
print(np.isnat(mixed))
print(mixed == np.datetime64("NaT"))
print(np.sort(mixed))
print(mixed[~np.isnat(mixed)])
print(mixed[0] + np.timedelta64(1, "D"), mixed[1] + np.timedelta64(1, "D"))

mask = mixed >= np.datetime64("2024-02-01")
print(mask)
print(mixed[mask])

# ── 05.5 Строки и datetime_as_string ───────────────────────────────────────
print("\n== 05.5 Строки ==")
dates = np.array(["2024-01-01", "2024-01-10", "2024-02-01"],
                 dtype="datetime64[D]")
print(np.datetime_as_string(dates))
print(np.datetime_as_string(dates, unit="M"))
print(np.datetime_as_string(np.datetime64("2024-01-01T10:30:45"), unit="m"))
print(dates.astype(str))

# ── 05.6 Python datetime туда и обратно ────────────────────────────────────
print("\n== 05.6 Python datetime ==")
from datetime import datetime

day = np.datetime64("2024-01-01")
converted = day.astype(datetime)
print(converted, type(converted).__name__)

stamp = np.datetime64("2024-01-01T10:30:45")
converted = stamp.astype(datetime)
print(converted, type(converted).__name__)

print(np.datetime64(datetime(2024, 1, 1, 10, 30)))
print(np.array([datetime(2024, 1, 1), datetime(2024, 2, 1)]).dtype)
print(np.array([datetime(2024, 1, 1), datetime(2024, 2, 1)],
               dtype="datetime64[us]"))

# ── 05.7 Таймзоны: их нет ──────────────────────────────────────────────────
print("\n== 05.7 Таймзоны ==")
import warnings
from datetime import datetime, timedelta, timezone

aware = datetime(2024, 1, 1, 12, 0, tzinfo=timezone(timedelta(hours=3)))
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    as_numpy = np.datetime64(aware)
print(as_numpy, as_numpy.dtype)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print(np.datetime64("2024-01-01T00:00+03:00"))
print(np.array([aware]).dtype)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print(np.array([aware], dtype="datetime64[us]"))

# ── 05.8 0-мерные и массивы ────────────────────────────────────────────────
print("\n== 05.8 0-d и массивы ==")
scalar = np.datetime64("2024-01-01")
array = np.array(scalar)
print(scalar.shape, array.shape)
print(type(scalar).__name__, type(array).__name__)
print(np.array(["2024-01-01"], dtype="datetime64[D]").shape)

# ── 06.1 Сценарий: диапазон дат ────────────────────────────────────────────
print("\n== 06.1 Диапазон дат ==")
days = np.arange("2024-01-01", "2024-02-01", dtype="datetime64[D]")
print(days[:3], "...", days[-1], "всего", days.size)

week = days[(days >= np.datetime64("2024-01-15"))
            & (days <= np.datetime64("2024-01-21"))]
print(week)
print("дней в неделе:", week.size)

# ── 06.2 Сценарий: временной ряд ───────────────────────────────────────────
print("\n== 06.2 Временной ряд ==")
hours = np.arange("2024-01-01T00", "2024-01-01T06:00",
                  dtype="datetime64[h]")
print(hours)
print("шаг:", hours[1] - hours[0])
print("от начала:", hours - hours[0])

# ── 06.3 Сценарий: длительности ────────────────────────────────────────────
print("\n== 06.3 Длительности ==")
events = np.array(["2024-01-01", "2024-01-10", "2024-02-01", "2024-03-15"],
                  dtype="datetime64[D]")
gaps = np.diff(events)
print(gaps, "итого:", gaps.sum())
print("в днях числом:", gaps / np.timedelta64(1, "D"))
print("в часах:", gaps.astype("timedelta64[h]"))

# ── 08.1 Задача: от заказа до доставки ─────────────────────────────────────
print("\n== 08.1 Задача: доставка ==")
ordered = np.array(["2024-02-28T09:15", "2024-03-01T18:40"],
                   dtype="datetime64[m]")
delivered = np.array(["2024-03-01T12:00", "2024-03-04T09:30"],
                     dtype="datetime64[m]")
wait = delivered - ordered
print(wait)
print("в часах:", wait.astype("timedelta64[h]"))

# ── 08.2 Задача: месяцы года ───────────────────────────────────────────────
print("\n== 08.2 Задача: месяцы ==")
months = np.arange("2024-01", "2025-01", dtype="datetime64[M]")
print(np.datetime_as_string(months))
print("всего:", months.size, "| от", months[0], "до", months[-1])
