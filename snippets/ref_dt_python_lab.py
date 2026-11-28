"""Справочник: Python datetime. Все примеры страницы ref-dt-python.html.

Требуется Python 3.12 (stdlib).
Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_dt_python_lab.py
"""

# ── 01. Как создать ────────────────────────────────────────────────────────
print("── 01. Как создать ──")
from datetime import date, datetime, time, timedelta

dt = datetime(2024, 3, 15, 14, 30, 45)
d = date(2024, 3, 15)
t = time(14, 30, 45)
delta = timedelta(days=2, hours=3, minutes=30)
print(dt)
print(d)
print(t)
print(delta)
print(dt.year, dt.month, dt.day, dt.hour, dt.minute)

# ── 02. Части момента ─────────────────────────────────────────────────────
print("\n── 02. Части момента ──")
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30, 45, 123456)
print(dt.isoformat())
print(dt.date().isoformat())
print(dt.time().isoformat())
print(dt.weekday(), dt.isoweekday())
print(dt.isocalendar())

# ── 03. naive и aware ─────────────────────────────────────────────────────
print("\n── 03. naive и aware ──")
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

naive = datetime(2024, 3, 15, 14, 30)
utc = naive.replace(tzinfo=timezone.utc)
moscow = naive.replace(tzinfo=ZoneInfo("Europe/Moscow"))
print(naive.isoformat())
print(utc.isoformat())
print(moscow.isoformat())
print(moscow.utcoffset())
print(moscow.tzinfo)

# ── 04. ISO-строки ────────────────────────────────────────────────────────
print("\n── 04. ISO-строки ──")
from datetime import datetime, timezone

raw = "2024-03-15T14:30:00+03:00"
dt = datetime.fromisoformat(raw)
print(dt)
print(dt.isoformat())
print(dt.astimezone(timezone.utc).isoformat())
print(datetime.fromisoformat("2024-03-15T11:30:00Z"))

# ── 05. strftime и strptime ───────────────────────────────────────────────
print("\n── 05. strftime и strptime ──")
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30, 45)
print(dt.strftime("%Y-%m-%d %H:%M"))
print(dt.strftime("%d.%m.%Y, %H:%M:%S"))
print(dt.strftime("%j"), dt.strftime("%V"))
parsed = datetime.strptime("15.03.2024 14:30", "%d.%m.%Y %H:%M")
print(parsed)

# ── 06. epoch: timestamp и fromtimestamp ──────────────────────────────────
print("\n── 06. epoch ──")
from datetime import datetime, timezone

stamp = 1704067200
dt = datetime.fromtimestamp(stamp, tz=timezone.utc)
print(dt.isoformat())
print(dt.timestamp())
print(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
print(int(datetime.fromtimestamp(0, tz=timezone.utc).timestamp()))

# ── 07. astimezone: перевод между зонами ─────────────────────────────────
print("\n── 07. astimezone ──")
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

utc = datetime(2024, 3, 15, 11, 30, tzinfo=timezone.utc)
moscow = utc.astimezone(ZoneInfo("Europe/Moscow"))
berlin = utc.astimezone(ZoneInfo("Europe/Berlin"))
print(utc.isoformat())
print(moscow.isoformat())
print(berlin.isoformat())
print(moscow == berlin)

# ── 08. Арифметика и replace ──────────────────────────────────────────────
print("\n── 08. Арифметика и replace ──")
from datetime import date, datetime, timedelta

d = date(2024, 3, 15)
print(d + timedelta(days=10))
print(d + timedelta(days=20))
print((date(2024, 4, 1) - d).days)
dt = datetime(2024, 1, 31, 10, 0)
print(dt.replace(month=2, day=1))
print((dt + timedelta(days=1)).isoformat())

# ── 09. DST: несуществующее и неоднозначное время ────────────────────────
print("\n── 09. DST ──")
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

berlin = ZoneInfo("Europe/Berlin")
spring = datetime(2024, 3, 31, 2, 30, tzinfo=berlin)
print(spring.isoformat())
print(spring.astimezone(timezone.utc).isoformat())
print(spring.astimezone(timezone.utc).astimezone(berlin).isoformat())
fall0 = datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=0)
fall1 = datetime(2024, 10, 27, 2, 30, tzinfo=berlin, fold=1)
print(fall0.isoformat(), fall0.utcoffset())
print(fall1.isoformat(), fall1.utcoffset())
w = datetime(2024, 3, 30, 12, tzinfo=berlin)
print((w + timedelta(days=1)).isoformat())
next_utc = w.astimezone(timezone.utc) + timedelta(days=1)
print(next_utc.astimezone(berlin).isoformat())

# ── 10. Сценарий: разбор ISO из API ───────────────────────────────────────
print("\n── 10. Разбор ISO из API ──")
from datetime import datetime, timezone

raw = "2024-03-15T14:30:00+03:00"
dt = datetime.fromisoformat(raw)
print(dt.isoformat())
print(dt.astimezone(timezone.utc).isoformat())
print(dt.utcoffset())

# ── 11. Сценарий: TTL и интервал ──────────────────────────────────────────
print("\n── 11. TTL и интервал ──")
from datetime import datetime, timedelta, timezone

created = datetime(2024, 3, 15, 14, 30, tzinfo=timezone.utc)
ttl = timedelta(hours=1, minutes=30)
expires = created + ttl
check_at = datetime(2024, 3, 15, 15, 45, tzinfo=timezone.utc)
print(created.isoformat())
print(expires.isoformat())
print(check_at < expires)
print((expires - created).total_seconds())

# ── 12. Сценарий: группировка по месяцам ─────────────────────────────────
print("\n── 12. Группировка по месяцам ──")
from collections import Counter
from datetime import datetime

stamps = [
    "2024-01-05T10:00:00",
    "2024-01-19T08:30:00",
    "2024-02-01T14:00:00",
    "2024-03-07T19:30:00",
    "2024-03-20T15:55:00",
]
by_month = Counter()
for raw in stamps:
    d = datetime.fromisoformat(raw).date().replace(day=1)
    by_month[d.isoformat()] += 1
print(dict(sorted(by_month.items())))

# ── 13. Задача: ISO с Z в московское время ───────────────────────────────
print("\n── 13. ISO с Z → Москва ──")
from datetime import datetime
from zoneinfo import ZoneInfo

dt = datetime.fromisoformat("2024-03-15T11:30:00Z")
print(dt.isoformat())
print(dt.astimezone(ZoneInfo("Europe/Moscow")).isoformat())

# ── 14. Задача: сколько дней до дедлайна ─────────────────────────────────
print("\n── 14. Дней до дедлайна ──")
from datetime import date

start = date(2024, 3, 15)
deadline = date(2024, 4, 1)
left = deadline - start
print(left.days)
print(left.total_seconds())
print(deadline > start)
