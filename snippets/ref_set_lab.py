"""Справочник: set. Все примеры страницы ref-set.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_set_lab.py

Порядок множества строк не гарантирован, поэтому в выводе используется
sorted(...) — иначе .out на странице нельзя было бы воспроизвести.
"""

# ── 03a. Как создать ───────────────────────────────────────────────────────
print("── 03a. Как создать ──")
tags = {"python", "sql"}                     # литерал
empty = set()                                # пустое множество, не {}
from_list = set(["Anna", "Anna", "Olga"])    # дубли схлопнутся
from_string = set("abc")                     # буквы строки
squares = {x * x for x in range(1, 5)}       # set comprehension
print(sorted(tags))
print(empty)
print(sorted(from_list))
print(sorted(from_string))
print(sorted(squares))

# ── 03b. {} — это dict ────────────────────────────────────────────────────
print("\n── 03b. {} — это dict ──")
empty_braces = {}
empty_set = set()
print(type(empty_braces).__name__, len(empty_braces))
print(type(empty_set).__name__, len(empty_set))

# ── 05a. add, remove, discard ──────────────────────────────────────────────
print("\n── 05a. add, remove, discard ──")
s = {"python", "sql"}
s.add("dbt")
s.add("python")                  # дубль ничего не меняет
print(sorted(s))

s.remove("dbt")                  # удаляет по значению
print(sorted(s))
s.discard("airflow")             # элемента нет — молча, без ошибки
print(sorted(s))

try:
    s.remove("airflow")          # а remove здесь бросит KeyError
except KeyError as e:
    print(type(e).__name__)

# ── 05b. pop и clear ───────────────────────────────────────────────────────
print("\n── 05b. pop и clear ──")
s = {"python", "sql", "pandas"}
removed = s.pop()                # какой именно элемент — не гарантировано
print(removed in {"python", "sql", "pandas"}, len(s))
s.clear()
print(len(s))

# ── 05c. update ────────────────────────────────────────────────────────────
print("\n── 05c. update ──")
a = {"python", "sql"}
a.update({"pandas", "dbt"})
print(sorted(a))
a.update(["airflow"])            # принимает любой итерируемый
print(sorted(a))

# ── 05d. update("abc") против add("abc") ──────────────────────────────────
print("\n── 05d. update строки ──")
s = set()
s.update("abc")                  # строка — итерируемое: добавляются буквы
print(sorted(s))

one = set()
one.add("abc")                   # одна строка целиком
print(sorted(one))

# ── 05e. union, intersection, difference, symmetric_difference ────────────
print("\n── 05e. Четыре операции ──")
a = {"python", "sql", "pandas"}
b = {"python", "dbt", "sql"}

print(sorted(a.union(b)))
print(sorted(a.intersection(b)))
print(sorted(a.difference(b)))
print(sorted(a.symmetric_difference(b)))

# ── 05f. *_update на месте ─────────────────────────────────────────────────
print("\n── 05f. *_update ──")
a = {"python", "sql", "pandas"}
b = {"python", "dbt"}

c = a.copy()
c.intersection_update(b)
print(sorted(c))

d = a.copy()
d.difference_update(b)
print(sorted(d))

e = a.copy()
e.symmetric_difference_update(b)
print(sorted(e))

# ── 05g. Операторы и отношения ─────────────────────────────────────────────
print("\n── 05g. Операторы ──")
a = {"python", "sql", "pandas"}
b = {"python", "dbt", "sql"}
print(sorted(a & b))
print(sorted(a | b))
print(sorted(a - b))
print(sorted(a ^ b))

small = {"python", "sql"}
print(small <= a, small < a)
print(a >= small, a > small)
print(small.issubset(a), a.issuperset(small))
print(a.isdisjoint({"java", "go"}))

# ── 05h. frozenset ─────────────────────────────────────────────────────────
print("\n── 05h. frozenset ──")
fs = frozenset({"read", "write"})
print(sorted(fs))

roles = {
    frozenset({"read", "write"}): "editor",
    frozenset({"read"}): "viewer",
}
print(roles[frozenset({"write", "read"})])   # порядок элементов не важен

try:
    fs.add("delete")             # frozenset неизменяем
except AttributeError as e:
    print(type(e).__name__)

print(fs <= frozenset({"read", "write", "delete"}))

# ── 06a. Сценарий: дедупликация ───────────────────────────────────────────
print("\n── 06a. Сценарий: дедупликация ──")
tags = ["sql", "python", "sql", "pandas", "python", "dbt"]
unique = set(tags)
print(len(tags), len(unique))
print(sorted(unique))
print(list(dict.fromkeys(tags)))     # порядок сохранён — это dict, не set

# ── 06b. Сценарий: общие теги ─────────────────────────────────────────────
print("\n── 06b. Сценарий: общие теги ──")
anna = {"python", "sql", "pandas", "airflow"}
olga = {"python", "dbt", "sql"}

print(sorted(anna & olga))       # общие
print(sorted(anna - olga))       # только у Анны
print(sorted(olga - anna))       # только у Ольги
print(anna.isdisjoint({"java", "go"}))

# ── 06c. Сценарий: участники и права ──────────────────────────────────────
print("\n── 06c. Сценарий: права ──")
participants = {"Anna", "Olga", "Ivan"}
new = {"Ivan", "Petr"}
print(sorted(participants | new))    # все участники
print(sorted(new - participants))    # кто пришёл впервые
print(sorted(participants & new))    # кто был и остался

role_by_permissions = {
    frozenset({"read"}): "viewer",
    frozenset({"read", "write"}): "editor",
}
print(role_by_permissions[frozenset({"write", "read"})])

# ── 08a. Задача: симметричная разность ────────────────────────────────────
print("\n── 08a. Задача: симметричная разность ──")
day1 = ["Anna", "Ivan", "Olga"]
day2 = ["Ivan", "Petr"]

only_one_day = set(day1) ^ set(day2)
print(sorted(only_one_day))

# ── 08b. Задача: кэш ролей по frozenset ───────────────────────────────────
print("\n── 08b. Задача: кэш ролей ──")
cache = {}

def role(perms):
    key = frozenset(perms)
    if key not in cache:
        cache[key] = "admin" if "write" in key else "viewer"
    return cache[key]

print(role({"read", "write"}))
print(role({"read"}))
print(role({"read", "write"}))   # уже из кэша
print(len(cache))
