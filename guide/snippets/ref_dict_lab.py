"""Справочник: dict. Все примеры страницы ref-dict.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_dict_lab.py
"""

# ── 01. Что это ─────────────────────────────────────────────────────────────
print("── 01. Что это ──")
prices = {"apple": 120, "pear": 90}
print(prices["apple"])
print(len(prices))

# ── 02. Когда брать ────────────────────────────────────────────────────────
print("\n── 02. Когда брать ──")
prices = {"apple": 120, "pear": 90}
print("pear" in prices)       # O(1) в среднем
print("plum" in prices)

# ── 03. Как создать ────────────────────────────────────────────────────────
print("\n── 03. Как создать ──")
empty = {}
pairs = dict([("a", 1), ("b", 2)])
flags = dict.fromkeys(["read", "write"], False)
squares = {x: x * x for x in range(1, 4)}
print(prices)
print(empty)
print(pairs)
print(flags)
print(squares)

# ── 04. get: безопасное чтение ─────────────────────────────────────────────
print("\n── 04. get ──")
print(prices.get("apple"))
print(prices.get("plum"))
print(prices.get("plum", 0))

# ── 05. setdefault: значение по умолчанию ─────────────────────────────────
print("\n── 05. setdefault ──")
d = {"a": 1}
print(d.setdefault("b", 0))     # создал ключ
print(d.setdefault("a", 999))   # не тронул существующий
print(d)

# ── 06. update, pop, popitem, del ─────────────────────────────────────────
print("\n── 06. update, pop, popitem ──")
d = {"a": 1, "b": 2}
d.update({"b": 3, "c": 4})
print(d)
print(d.pop("c"))
print(d.pop("zzz", "нет"))
print(d.popitem())              # пара, вставленная последней
del d["a"]
print(d)

# ── 07. keys, values, items ───────────────────────────────────────────────
print("\n── 07. keys, values, items ──")
prices = {"apple": 120, "pear": 90}
print(list(prices.keys()))
print(list(prices.values()))
print(list(prices.items()))

view = prices.keys()
prices["plum"] = 70
print(list(view))               # view живой: видит новый ключ

# ── 08. Порядок вставки ───────────────────────────────────────────────────
print("\n── 08. Порядок вставки ──")
d = {"b": 2, "a": 1}
d["c"] = 3
print(list(d))

# ── 09. Объединение через | ───────────────────────────────────────────────
print("\n── 09. Объединение ──")
base = {"a": 1, "b": 2}
extra = {"b": 20, "c": 30}
print(base | extra)
base |= {"d": 4}
print(base)

# ── 10. Копия и алиас ─────────────────────────────────────────────────────
print("\n── 10. Копия и алиас ──")
a = {"x": 1}
alias = a
copy = a.copy()
alias["y"] = 2
copy["z"] = 3
print(a)
print(copy)

# ── 11. Сценарий: счётчик ─────────────────────────────────────────────────
print("\n── 11. Сценарий: счётчик ──")
words = ["sql", "python", "sql", "dbt"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)

# ── 12. Сценарий: группировка ─────────────────────────────────────────────
print("\n── 12. Сценарий: группировка ──")
orders = [("Anna", 1200), ("Ivan", 800), ("Anna", 500)]
groups = {}
for user, amount in orders:
    groups.setdefault(user, []).append(amount)
print(groups)

# ── 13. Сценарий: реестр обработчиков ────────────────────────────────────
print("\n── 13. Сценарий: реестр ──")
handlers = {"GET": "list_users", "POST": "create_user"}
print(handlers.get("DELETE"))
print(handlers.get("DELETE", "404"))

# ── 14. Ключом может быть только hashable ─────────────────────────────────
print("\n── 14. Hashable ключ ──")
grid = {(10, 20): "start"}
print(grid[(10, 20)])

# ── 15. Ловушка fromkeys ─────────────────────────────────────────────────
print("\n── 15. Ловушка fromkeys ──")
d = dict.fromkeys(["a", "b"], [])
d["a"].append(1)
print(d)
