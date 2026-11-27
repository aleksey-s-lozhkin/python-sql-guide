"""Справочник: Counter. Все примеры страницы ref-counter.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_counter_lab.py
"""

from collections import Counter

# ── 01. Что это и как устроено ─────────────────────────────────────────────
print("── 01. Что это ──")
words = ["sql", "python", "sql", "pandas", "python", "sql"]
counts = Counter(words)
print(dict(counts))
print(counts["sql"])
print(counts["rust"], "rust" in counts)
print(len(counts))

# ── 03. Как создать ────────────────────────────────────────────────────────
print("\n── 03. Как создать ──")
print(dict(Counter(["a", "b", "a"])))     # из итерируемого
print(dict(Counter({"a": 2, "b": 1})))    # из словаря
print(dict(Counter(a=3, b=1)))            # из именованных аргументов
print(dict(Counter("abracadabra")))       # строка — тоже итерируемое
print(Counter())                          # пустой счётчик

# ── 05.1. Частоты и отсутствующий ключ ─────────────────────────────────────
print("\n── 05.1. Частоты и отсутствующий ключ ──")
counts = Counter("abracadabra")
print(counts["a"])
print(counts["z"])               # нет ключа — 0, без KeyError
print("z" in counts)             # но ключ не создан
counts["a"] += 100               # запись как в обычном dict
print(dict(counts))

# ── 05.2. most_common: топ-N ───────────────────────────────────────────────
print("\n── 05.2. most_common ──")
cities = ["Москва", "Казань", "Москва", "Омск", "Казань", "Москва", "Сочи"]
counts = Counter(cities)
print(counts.most_common(2))
print(counts.most_common())      # полная сортировка по убыванию
print(counts.most_common(10))    # больше, чем ключей — вернутся все

# ── 05.3. elements и total ─────────────────────────────────────────────────
print("\n── 05.3. elements и total ──")
counts = Counter({"a": 2, "b": 1, "c": 0, "d": -1})
print(list(counts.elements()))   # только положительные счётчики
print(counts.total())            # сумма всех счётчиков

# ── 05.4. update и subtract ────────────────────────────────────────────────
print("\n── 05.4. update и subtract ──")
counts = Counter({"python": 2, "sql": 1})
counts.update(["python", "pandas"])   # складывает, а не заменяет
counts.update({"sql": 2})
print(dict(counts))

counts.subtract({"python": 3, "sql": 10})   # вычитает и уходит в минус
print(dict(counts))

# ── 05.5. Арифметика: + - & | ─────────────────────────────────────────────
print("\n── 05.5. Арифметика ──")
a = Counter({"python": 3, "sql": 1})
b = Counter({"python": 1, "sql": 2})
print(dict(a + b))    # складывает счётчики
print(dict(a - b))    # вычитает, неположительные выбрасывает
print(dict(a & b))    # минимум по каждому ключу
print(dict(a | b))    # максимум по каждому ключу

# ── 05.6. Нули, минусы и унарные операторы ─────────────────────────────────
print("\n── 05.6. Нули, минусы, унарные ──")
a = Counter({"python": 4, "sql": 1})
b = Counter({"python": 1, "sql": 5})
print(dict(a - b))            # sql ушёл в минус — пара исчезла

a.subtract(b)                 # subtract меняет на месте
print(dict(a))                # нули и минусы остаются
print(a.total())              # total() суммирует всё, включая минусы

c = Counter({"a": 2, "b": 0, "c": -3})
print(dict(+c))               # унарный + — только положительные
print(dict(-c))               # унарный - — знак меняется, мусор отброшен
print(Counter({"a": 0}) == Counter())

# ── 05.7. copy и clear ─────────────────────────────────────────────────────
print("\n── 05.7. copy и clear ──")
counts = Counter("abracadabra")
copy = counts.copy()
counts.clear()
print(copy["a"], len(counts), len(copy))

# ── 06.1. Сценарий: частоты статусов ───────────────────────────────────────
print("\n── 06.1. Частоты статусов ──")
statuses = ["new", "paid", "new", "shipped", "paid", "new", "cancelled"]
by_status = Counter(statuses)
print(dict(by_status))
print(by_status.most_common(2))
print(by_status.total())

# ── 06.2. Сценарий: топ-N городов ──────────────────────────────────────────
print("\n── 06.2. Топ-N городов ──")
city_orders = ["Москва", "Казань", "Москва", "Омск", "Казань",
               "Москва", "Сочи", "Москва", "Омск", "Казань"]
top = Counter(city_orders).most_common(3)
print(top)
for city, n in top:
    print(f"{city}: {n}")

# ── 06.3. Сценарий: сравнение двух наборов ────────────────────────────────
print("\n── 06.3. Сравнение наборов ──")
warehouse = Counter({"яблоко": 10, "груша": 5, "слива": 8})
sold = Counter({"яблоко": 12, "груша": 3, "слива": 8})
print(dict(warehouse - sold))   # чего не хватает на складе
print(dict(sold - warehouse))   # переизбыток
print(dict(warehouse & sold))   # пересечение мультимножеств
print(warehouse == sold)        # равенство частот

# ── 08.1. Задача: топ-3 слова ──────────────────────────────────────────────
print("\n── 08.1. Топ-3 слова ──")
text = "SQL python sql pandas python SQL"
counts = Counter(text.lower().split())
print(counts.most_common(3))

# ── 08.2. Задача: анаграммы ────────────────────────────────────────────────
print("\n── 08.2. Анаграммы ──")
def is_anagram(a: str, b: str) -> bool:
    return Counter(a.lower()) == Counter(b.lower())

print(is_anagram("listen", "Silent"))
print(is_anagram("abc", "abbc"))
