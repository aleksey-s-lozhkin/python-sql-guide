"""Справочник: defaultdict. Все примеры страницы ref-defaultdict.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_defaultdict_lab.py
"""

import functools
import pickle
from collections import defaultdict

# ── 01. Что это и как устроено ─────────────────────────────────────────────
print("── 01. Что это ──")
orders = [("Anna", 1200), ("Ivan", 800), ("Anna", 500)]
by_user = defaultdict(list)
for user, amount in orders:
    by_user[user].append(amount)

print(dict(by_user))
print(by_user.default_factory)

# ── 03. Как создать ────────────────────────────────────────────────────────
print("\n── 03. Как создать ──")
print(defaultdict(list))                 # фабрика — list
print(defaultdict(int)["missing"])       # фабрика int → 0
d = defaultdict(list, {"Anna": [1200]})  # можно сразу с данными
print(dict(d))
print(defaultdict(None))                 # фабрики нет

# ── 05.1. Чтение создаёт ключ ──────────────────────────────────────────────
print("\n── 05.1. Чтение создаёт ключ ──")
d = defaultdict(int)
print(d["x"])            # фабрика int() → 0
print("x" in d)          # ключ уже в словаре
print(d.get("y"))        # get фабрику не зовёт
print("y" in d)          # и ключ не создаёт
print(dict(d))

# ── 05.2. default_factory и None ───────────────────────────────────────────
print("\n── 05.2. default_factory ──")
d = defaultdict(list)
print(d.default_factory)
d["a"].append(1)
print(dict(d))

d.default_factory = int          # фабрика меняется на лету
print(d["b"])
print(dict(d))

plain = defaultdict(None)        # фабрики нет — ведёт себя как dict
try:
    plain["x"]
except KeyError as e:
    print("KeyError", e)

# ── 05.3. Унаследованные методы dict ──────────────────────────────────────
print("\n── 05.3. Методы dict ──")
d = defaultdict(int, {"a": 1})
print(d.get("b"))                # None, ключ не создан
print(d.setdefault("c", 5))      # фабрика не вызывается
print(d.pop("a"))
print(list(d.items()))
d.update({"e": 7})
print(dict(d))

# ── 05.4. copy() сохраняет фабрику ────────────────────────────────────────
print("\n── 05.4. copy ──")
d = defaultdict(list, {"Anna": [1200]})
copy = d.copy()
copy["Ivan"].append(800)
print(dict(copy))
print(copy.default_factory is list)
copy["Anna"].append(500)         # копия поверхностная
print(dict(d))

# ── 05.5. __missing__ ──────────────────────────────────────────────────────
print("\n── 05.5. __missing__ ──")
class Logged(defaultdict):
    def __missing__(self, key):
        print("создаю", key)
        return super().__missing__(key)

d = Logged(list)
d["Anna"].append(1200)
d["Anna"].append(500)
print(dict(d))

# ── 05.6. pickling: lambda против partial ─────────────────────────────────
print("\n── 05.6. pickle ──")
try:
    pickle.dumps(defaultdict(lambda: 0))
except Exception as e:
    print(type(e).__name__)

nested = defaultdict(functools.partial(defaultdict, int))
nested["Anna"]["x"] += 1
restored = pickle.loads(pickle.dumps(nested))
print(restored["Anna"]["x"])
print(restored["Ivan"]["y"])     # фабрика восстановилась
print(type(restored.default_factory).__name__)

# ── 06.1. Сценарий: группировка и счётчик ─────────────────────────────────
print("\n── 06.1. Группировка и счётчик ──")
orders = [
    ("Anna", 1200),
    ("Ivan", 800),
    ("Anna", 500),
    ("Olga", 1500),
]
by_user = defaultdict(list)
totals = defaultdict(int)
for user, amount in orders:
    by_user[user].append(amount)
    totals[user] += amount

print(dict(by_user))
print(dict(totals))
print(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

# ── 06.2. Сценарий: список смежности и инверсия ───────────────────────────
print("\n── 06.2. Граф и инверсия ──")
edges = [("Anna", "Ivan"), ("Anna", "Olga"), ("Ivan", "Olga")]
graph = defaultdict(list)
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)          # неориентированный граф
print(dict(graph))

prices = {"apple": 120, "pear": 90, "plum": 120}
by_price = defaultdict(list)
for name, price in prices.items():
    by_price[price].append(name)
print(dict(by_price))

# ── 06.3. Сценарий: вложенные defaultdict ─────────────────────────────────
print("\n── 06.3. Вложенные ──")
orders = [("Москва", 2023), ("Казань", 2023), ("Москва", 2024), ("Москва", 2024)]
by_city_year = defaultdict(lambda: defaultdict(int))
for city, year in orders:
    by_city_year[city][year] += 1

print(dict(by_city_year["Москва"]))
print(dict(by_city_year["Казань"]))
print(by_city_year["Омск"][2024])   # создалась целая ветка
print(sorted(by_city_year))

# ── 08.1. Задача: группировка по длине слова ──────────────────────────────
print("\n── 08.1. Группировка по длине слова ──")
words = ["sql", "python", "dbt", "pandas", "go", "api"]
by_len = defaultdict(list)
for word in words:
    by_len[len(word)].append(word)
print(dict(by_len))

# ── 08.2. Задача: степени вершин ──────────────────────────────────────────
print("\n── 08.2. Степени вершин ──")
edges = [("Anna", "Ivan"), ("Anna", "Olga"), ("Ivan", "Olga"), ("Olga", "Ivan")]
degree = defaultdict(int)
for a, b in edges:
    degree[a] += 1
    degree[b] += 1
print(dict(degree))
