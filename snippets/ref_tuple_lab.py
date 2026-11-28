"""Справочник: tuple. Все примеры страницы ref-tuple.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_tuple_lab.py
"""

# ── 03a. Как создать ───────────────────────────────────────────────────────
print("── 03a. Как создать ──")
point = (10, 20)                 # литерал
single = (42,)                   # запятая обязательна
empty = ()
from_list = tuple([1, 2, 3])     # из итерируемого
nested = ((10, 20), (30, 40))    # вложенные tuple
name = ("Anna", 1200)
print(point)
print(single)
print(empty)
print(from_list)
print(nested)
print(name)

# ── 03b. (1) против (1,) ───────────────────────────────────────────────────
print("\n── 03b. (1) против (1,) ──")
not_tuple = (1)                  # это int в скобках
one = (1,)                       # tuple из одного элемента
print(type(not_tuple).__name__, type(one).__name__, len(one))

# ── 05a. Методы count и index ──────────────────────────────────────────────
print("\n── 05a. count и index ──")
orders = ("Anna", "Ivan", "Anna", "Olga")
print(orders.count("Anna"))
print(orders.index("Ivan"))
print(orders.index("Anna"))      # первое вхождение, а не второе

# ── 05b. Операторы +, *, in, сравнение ────────────────────────────────────
print("\n── 05b. Операторы ──")
a = (1, 2)
print(a + (3,))                  # новый tuple
print(a * 3)                     # повторение ссылок
print(len(a), 2 in a)            # in — перебор, O(n)
print(a == (1, 2), a < (1, 3))   # сравнение по элементам

# ── 05c. Срезы ─────────────────────────────────────────────────────────────
print("\n── 05c. Срезы ──")
point = (10, 20, 30, 40, 50)
print(point[0], point[-1])
print(point[1:4])                # срез tuple — тоже tuple
print(point[::2])
print(point[::-1])

# ── 05d. Распаковка ────────────────────────────────────────────────────────
print("\n── 05d. Распаковка ──")
record = ("Anna", 1200, "2024-05-01")
name, amount, day = record
print(name, amount, day)

first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)

print(*record, sep=" | ")        # распаковка в аргументы print

# ── 05e. hash и ключ словаря ──────────────────────────────────────────────
print("\n── 05e. hash и ключ ──")
point = (10, 20)
grid = {point: "start"}
print(grid[(10, 20)])
print(point in grid)
print(len({(1, 2), (1, 2), (3, 4)}))

box = (1, [2, 3])                # tuple с изменяемым элементом
try:
    {box}
except TypeError as e:
    print(type(e).__name__)

# ── 05f. namedtuple ────────────────────────────────────────────────────────
print("\n── 05f. namedtuple ──")
from collections import namedtuple

Point = namedtuple("Point", "x y")
p = Point(10, 20)
print(p)
print(p.x, p.y)
print(p._replace(x=99))          # новый объект, исходный не меняется
print(p)

# ── 05g. dataclass(frozen=True) ───────────────────────────────────────────
print("\n── 05g. dataclass ──")
from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True)
class Order:
    user: str
    amount: int

o = Order("Anna", 1200)
print(o)
print(o.user)
try:
    o.amount = 500               # поля заморожены
except FrozenInstanceError as e:
    print(type(e).__name__)

# ── 05h. += создаёт новый объект ──────────────────────────────────────────
print("\n── 05h. += и tuple ──")
def add_item(record, item):
    record += (item,)            # для tuple это новый объект и новая привязка
    return record

original = ("Anna",)
updated = add_item(original, "Olga")
print(original)
print(updated)

# ── 05i. Повторение tuple с вложенным списком ─────────────────────────────
print("\n── 05i. t * 2 ──")
row = ([1],)
doubled = row * 2
doubled[0].append(2)             # обе позиции смотрят на один список
print(doubled)
print(row)

# ── 06a. Сценарий: запись заказа и * ──────────────────────────────────────
print("\n── 06a. Сценарий: запись ──")
order = ("Anna", 1200, "2024-05-01", "paid", "gift")
user, amount, day, *flags = order
print(user, amount, day)
print(flags)

# ── 06b. Сценарий: составной ключ ─────────────────────────────────────────
print("\n── 06b. Сценарий: ключ ──")
orders = [
    ("Anna", "2024-05-01", 1200),
    ("Anna", "2024-05-01", 500),
    ("Olga", "2024-05-01", 1500),
    ("Ivan", "2024-05-02", 800),
]
totals = {}
for user, day, amount in orders:
    key = (user, day)            # составной ключ
    totals[key] = totals.get(key, 0) + amount

for key in sorted(totals):
    print(key, totals[key])

# ── 06c. Сценарий: возврат нескольких значений ────────────────────────────
print("\n── 06c. Сценарий: возврат значений ──")
def order_stats(amounts):
    return min(amounts), max(amounts), sum(amounts)

low, high, total = order_stats([1200, 800, 1500])
print(low, high, total)

orders = [("Anna", 1200), ("Olga", 1500), ("Ivan", 800)]
first, *other = orders
print(first)
print(other)

# ── 08a. Задача: уникальные пары ──────────────────────────────────────────
print("\n── 08a. Задача: уникальные пары ──")
pairs = [("Anna", "IT"), ("Ivan", "Sales"), ("Anna", "IT"), ("Olga", "IT")]
unique = list(dict.fromkeys(pairs))
print(unique)

# ── 08b. Задача: namedtuple из строки ─────────────────────────────────────
print("\n── 08b. Задача: namedtuple ──")
from collections import namedtuple

Order = namedtuple("Order", "user amount")
row = ("Anna", 1200)
order = Order(*row)
print(order)
print(order._asdict())
