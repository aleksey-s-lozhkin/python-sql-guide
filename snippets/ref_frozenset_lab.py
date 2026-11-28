"""Справочник: frozenset. Все примеры страницы ref-frozenset.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_frozenset_lab.py

Вывод не зависит от машины: нет времени, id() и значений hash().
Множества строк печатаются через sorted(...), иначе .out на странице
нельзя было бы воспроизвести. Блоки файла совпадают с блоками страницы:
сначала код, затем ровно его вывод.
"""

import json

# ── 03. Как создать ────────────────────────────────────────────────────────
print("── 03. Как создать ──")
empty = frozenset()                                  # пустой frozenset
from_list = frozenset(["Anna", "Olga", "Anna"])      # дубли схлопнутся
from_string = frozenset("abc")                       # буквы строки
from_range = frozenset(range(1, 5))                  # из range
from_set = frozenset({"read", "write"})              # из set
from_dict = frozenset({"read": 1, "write": 2})       # ключи словаря
copy = frozenset(from_set)                           # из другого frozenset
print(empty)
print(from_range)
print(sorted(from_list))
print(sorted(from_string))
print(sorted(from_set))
print(sorted(from_dict))
print(copy == from_set, type(copy).__name__)

# ── 05.1. Неизменяемость: нет методов, изменение — новый объект ────────────
print("\n── 05.1. Неизменяемость ──")
fs = frozenset({1, 2})
modifiers = [
    "add", "remove", "discard", "pop", "clear", "update",
    "intersection_update", "difference_update", "symmetric_difference_update",
]
print([name for name in modifiers if hasattr(fs, name)])
try:
    fs.add(3)                    # у set метод есть, у frozenset — нет
except AttributeError as e:
    print(type(e).__name__, e)
print(sorted(fs))

alias = fs
fs |= {3}                        # это переприсваивание, а не мутация
print(sorted(alias), sorted(fs))
print(alias is fs, alias == fs)

# ── 05.2. Hashable: ключ, элемент, вложение ────────────────────────────────
print("\n── 05.2. Hashable ──")
read_write = frozenset({"read", "write"})
print(hash(read_write) == hash(frozenset({"write", "read"})))
role_by_perms = {
    frozenset({"read"}): "viewer",
    frozenset({"read", "write"}): "editor",
}
print(role_by_perms[frozenset({"write", "read"})])
pool = {frozenset({1, 2}), frozenset({2, 1}), frozenset({3})}
print(len(pool), sorted(sorted(perms) for perms in pool))
nested = frozenset({frozenset({1}), frozenset({1, 2})})
print(len(nested), frozenset({1, 2}) in nested)

a = frozenset({1, 2})
b = frozenset({2, 1})
print(a == b, hash(a) == hash(b))
print(a == {2, 1}, type(a == {2, 1}).__name__)

# ── 05.3. Операции и тип результата ────────────────────────────────────────
print("\n── 05.3. Операции и тип результата ──")
a = frozenset({"python", "sql", "pandas"})
b = frozenset({"python", "dbt", "sql"})
print(sorted(a.union(b)))
print(sorted(a.intersection(b)))
print(sorted(a.difference(b)))
print(sorted(a.symmetric_difference(b)))
print(sorted(a.union(["airflow"])))              # метод принимает итерируемый
print(sorted(a.intersection(["sql", "java"])))
print(sorted(a.difference(["sql"])))
print(sorted(a.symmetric_difference(("python", "go"))))

fs = frozenset({1, 2})
ms = {2, 3}
print(type(fs | ms).__name__, sorted(fs | ms))
print(type(ms | fs).__name__, sorted(ms | fs))
print(type(fs & ms).__name__, type(ms & fs).__name__)
print(type(fs - ms).__name__, type(ms - fs).__name__)
print(type(fs ^ ms).__name__, type(ms ^ fs).__name__)
print(type(fs.union(ms)).__name__)
print(fs.copy() is fs, type(fs.copy()).__name__)

# ── 05.4. Отношения и встроенные функции ───────────────────────────────────
print("\n── 05.4. Отношения и встроенные функции ──")
a = frozenset({"read", "write"})
print(a.issubset({"read", "write", "delete"}))
print(a.issuperset({"read"}))
print(a.isdisjoint({"admin", "delete"}))
print(a <= {"read", "write"}, a < {"read", "write"})
print(a >= {"read"}, a > {"read"})
print("read" in a, len(a), sorted(x for x in a))
print(bool(a), bool(frozenset()))

# ── 06.1. Сценарий: реестр ролей и кэш ─────────────────────────────────────
print("\n── 06.1. Сценарий: реестр ролей и кэш ──")
role_by_perms = {
    frozenset({"read"}): "viewer",
    frozenset({"read", "write"}): "editor",
    frozenset({"read", "write", "delete"}): "admin",
}
raw_perms = ["write", "read", "write"]       # пришло из API, с дублем
key = frozenset(raw_perms)
print(key in role_by_perms, role_by_perms[key])

cache = {}

def role(perms):
    key = frozenset(perms)
    if key not in cache:
        cache[key] = role_by_perms.get(key, "viewer")
    return cache[key]

print(role({"read"}), role(["write", "read"]), role({"read"}))
print(len(cache))

# ── 06.2. Сценарий: набор прав как ключ ────────────────────────────────────
print("\n── 06.2. Сценарий: набор прав как ключ ──")
users = {
    "Anna": {"read", "write"},
    "Olga": {"read"},
    "Ivan": {"read", "write", "delete"},
}
by_perms = {}
for user, perms in users.items():
    by_perms.setdefault(frozenset(perms), []).append(user)
for perms, people in sorted(by_perms.items(), key=lambda kv: sorted(kv[0])):
    print(sorted(perms), sorted(people))

# ── 06.3. Сценарий: дедупликация комбинаций ────────────────────────────────
print("\n── 06.3. Сценарий: дедупликация комбинаций ──")
pairs = [
    frozenset({"Anna", "Olga"}),
    frozenset({"Olga", "Anna"}),      # тот же набор
    frozenset({"Ivan", "Anna"}),
    frozenset({"Ivan", "Anna"}),      # повтор
]
unique = set(pairs)
print(len(pairs), len(unique))
for pair in sorted(unique, key=sorted):
    print(sorted(pair))

# ── 07. Проверка ошибок ────────────────────────────────────────────────────
print("\n── 07. Проверка ошибок ──")
fs = frozenset({1, 2})
try:
    fs.add(3)
except AttributeError as e:
    print(type(e).__name__, e)
try:
    fs.update({3})
except AttributeError as e:
    print(type(e).__name__)

alias = fs
fs |= {3}
print(alias is fs, sorted(alias), sorted(fs))

for bad in ([[1, 2]], [{1, 2}]):
    try:
        frozenset(bad)               # текст сообщения зависит от версии
    except TypeError as e:
        print(type(e).__name__)

try:
    json.dumps({"perms": frozenset({"read"})})
except TypeError as e:
    print(type(e).__name__, e)
print(json.dumps({"perms": sorted(frozenset({"read", "write"}))}))

try:
    fs[0]
except TypeError as e:
    print(type(e).__name__, e)
print(frozenset({"read"}) == {"read"}, isinstance(fs, set), isinstance(fs, frozenset))

# ── 08a. Задача: недостающие права ─────────────────────────────────────────
print("\n── 08a. Задача: недостающие права ──")
REQUIRED = frozenset({"read", "write", "delete"})
current = {"read", "write"}
missing = REQUIRED - current
print(type(missing).__name__, len(missing), sorted(missing))
print(REQUIRED - REQUIRED == frozenset())

# ── 08b. Задача: фильтр по запрещённым тегам ───────────────────────────────
print("\n── 08b. Задача: фильтр по запрещённым тегам ──")
BLOCKED = frozenset({"adult", "spam", "violence"})
posts = [
    ("post-1", {"python", "sql"}),
    ("post-2", {"python", "spam"}),
    ("post-3", {"pandas", "adult", "sql"}),
]
for post_id, tags in posts:
    print(post_id, BLOCKED.isdisjoint(tags))
allowed = [post_id for post_id, tags in posts if BLOCKED.isdisjoint(tags)]
print(allowed)
