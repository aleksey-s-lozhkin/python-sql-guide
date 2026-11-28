"""Дата и время: лаборатория к главе 27.

Требуется pandas 3.0.1 (как в книге) и Python 3.12.
Запуск из корня проекта:
    python3 guide/snippets/27_datetime_lab.py

Все моменты фиксированные: now(), today() и random() не используются.
Системная зона тоже не участвует — все зоны указаны явно.
"""

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pandas as pd

# ── 06.1. Три сущности: момент, дата, длительность ─────────────────────────
print("── 06.1. Три сущности ──")
moment = datetime(2024, 3, 15, 12, 30, tzinfo=timezone.utc)
day = date(2024, 3, 15)
duration = timedelta(hours=2, minutes=15)
print(moment)
print(day)
print(duration)

# ── 06.2. aware и naive, перевод между зонами ─────────────────────────────
print("\n── 06.2. aware, naive и зоны ──")
naive = datetime(2024, 3, 15, 12, 30)
aware = naive.replace(tzinfo=timezone.utc)
moscow = aware.astimezone(ZoneInfo("Europe/Moscow"))
tokyo = aware.astimezone(ZoneInfo("Asia/Tokyo"))
print(naive)
print(aware)
print(moscow)
print(tokyo)
print(naive.tzinfo)
print(aware.tzinfo)

# ── 06.3. Epoch: секунды и миллисекунды ───────────────────────────────────
print("\n── 06.3. Epoch ──")
epoch = aware.timestamp()
print(int(epoch))
print(datetime.fromtimestamp(epoch, tz=timezone.utc))
print(datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat())

ms = 1710505800123
print(datetime.fromtimestamp(ms / 1000, tz=timezone.utc))
print(pd.Timestamp(ms, unit="ms", tz="UTC"))

# ── 06.4. Арифметика и ISO 8601 ───────────────────────────────────────────
print("\n── 06.4. Арифметика и ISO ──")
start = datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc)
end = datetime(2024, 3, 15, 12, 30, tzinfo=timezone.utc)
delta = end - start
print(delta)
print(delta.total_seconds())
print(start + timedelta(days=1))
print((start + timedelta(days=30)).date())

text = "2024-03-15T12:30:00+00:00"
parsed = datetime.fromisoformat(text)
print(parsed)
print(parsed.isoformat())
print(parsed.strftime("%d.%m.%Y %H:%M"))

# ── 06.5. DST: несуществующее и неоднозначное время ───────────────────────
print("\n── 06.5. DST ──")
berlin = ZoneInfo("Europe/Berlin")

# 1. Арифметика по «настенным часам»: +1 час даёт несуществующее время
before = datetime(2024, 3, 31, 1, 30, tzinfo=berlin)
wall_plus = before + timedelta(hours=1)
print(before)
print(wall_plus)
print(wall_plus.utcoffset())

# 2. Правильно: прибавляем час к моменту (UTC) и возвращаемся в зону
after = (before.astimezone(timezone.utc) + timedelta(hours=1)).astimezone(berlin)
print(after)
print(after.utcoffset())

# 3. Осенний переход: 02:30 встречается дважды
fold0 = datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=0)
fold1 = datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=1)
print(fold0.utcoffset(), fold1.utcoffset())

# ── 06.6. pandas: to_datetime, .dt и to_period ────────────────────────────
print("\n── 06.6. pandas: даты и .dt ──")
orders = pd.DataFrame(
    {
        "user": ["Anna", "Ivan", "Olga", "Anna", "Ivan"],
        "amount": [1200, 800, 1500, 500, 300],
        "created_at": [
            "2024-01-05 10:00",
            "2024-02-06 12:30",
            "2024-02-15 09:15",
            "2024-03-01 18:00",
            "2024-03-20 08:05",
        ],
    }
)
orders["created_at"] = pd.to_datetime(orders["created_at"])
print(orders["created_at"].dtype)
print(orders["created_at"].dt.month.tolist())
print(orders["created_at"].dt.dayofweek.tolist())

monthly = orders.groupby(orders["created_at"].dt.to_period("M"))["amount"].sum()
print(monthly)

# ── 06.7. pandas: tz_localize и tz_convert ────────────────────────────────
print("\n── 06.7. pandas: зоны ──")
ts_utc = pd.Timestamp("2024-03-15 12:30", tz="UTC")
print(ts_utc)
print(ts_utc.tz_convert("Europe/Moscow"))
print(ts_utc.tz_convert("Asia/Tokyo"))

naive_ts = pd.Timestamp("2024-03-15 12:30")
print(naive_ts.tz_localize("Europe/Berlin"))
print(naive_ts.tz_localize("UTC"))

# ── 07.1. Одна задача: месячная выручка на чистом Python ──────────────────
print("\n── 07.1. Python: месячная выручка ──")
rows = [
    ("Anna", "2024-01-05", 75000),
    ("Ivan", "2024-01-06", 1800),
    ("Anna", "2024-01-15", 1350),
    ("Olga", "2024-02-01", 1500),
    ("Ivan", "2024-02-10", 22000),
    ("Maria", "2024-02-20", 2250),
    ("Anna", "2024-03-03", 600),
    ("", "2024-03-07", 900),
    ("Olga", "2024-03-15", 75000),
    ("Petr", "2024-03-20", 22000),
]
by_month = {}
for user, day_text, revenue in rows:
    month = datetime.fromisoformat(day_text).strftime("%Y-%m")
    by_month[month] = by_month.get(month, 0) + revenue

for month in sorted(by_month):
    print(month, by_month[month])

# ── 07.2. Одна задача: то же в pandas ─────────────────────────────────────
print("\n── 07.2. pandas: месячная выручка ──")
df = pd.DataFrame(rows, columns=["user", "created_at", "revenue"])
df["created_at"] = pd.to_datetime(df["created_at"])
monthly = df.groupby(df["created_at"].dt.to_period("M"))["revenue"].sum()
print(monthly)
print(monthly.sum())

# ── 07.3. TZ-конверсия в Python ───────────────────────────────────────────
print("\n── 07.3. Python: AT TIME ZONE ──")
moment = datetime(2024, 3, 15, 12, 30, tzinfo=timezone.utc)
print(moment.astimezone(ZoneInfo("Europe/Moscow")))
print(moment.astimezone(ZoneInfo("Asia/Tokyo")))

# ── 07.4. TZ-конверсия в pandas ───────────────────────────────────────────
print("\n── 07.4. pandas: AT TIME ZONE ──")
ts = pd.Timestamp("2024-03-15 12:30", tz="UTC")
print(ts.tz_convert("Europe/Moscow"))
print(ts.tz_convert("Asia/Tokyo"))

# ── 10.1. Задача: epoch в миллисекундах ───────────────────────────────────
print("\n── 10.1. Задача: epoch в миллисекундах ──")
ms = 1710505800123
moment = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
print(moment)
print(moment.isoformat())
print(int(moment.timestamp() * 1000))

# ── 10.2. Задача: начало и конец месяца ──────────────────────────────────
print("\n── 10.2. Задача: границы месяца ──")
moment = datetime(2024, 3, 15, 12, 30, tzinfo=timezone.utc)
start = moment.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
if start.month == 12:
    next_month = start.replace(year=start.year + 1, month=1)
else:
    next_month = start.replace(month=start.month + 1)
print(start.isoformat())
print(next_month.isoformat())
print(start <= moment < next_month)
