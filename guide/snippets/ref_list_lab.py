"""Справочник: list. Все примеры страницы ref-list.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_list_lab.py
"""

# ── 01. Что это ─────────────────────────────────────────────────────────────
print("── 01. Что это ──")
rows = [10, 20, 30]
print(rows[1])            # доступ по индексу
print(rows[-1])           # отрицательный индекс — с конца
print(len(rows))

# ── 02. Когда брать ────────────────────────────────────────────────────────
print("\n── 02. Когда брать ──")
users = ["anna", "ivan", "olga"]
print(users[0], users[1:])      # порядок и срезы
print("ivan" in users)          # проверка входа O(n)

# ── 03. Как создать ────────────────────────────────────────────────────────
print("\n── 03. Как создать ──")
rows = [10, 20, 30]
empty = []
squares = [x * x for x in range(1, 5)]
names = ["Anna", "Olga"]
pairs = list(zip(names, [1200, 900]))
print(rows)
print(empty)
print(squares)
print(pairs)

# ── 04. Добавление ─────────────────────────────────────────────────────────
print("\n── 04. Добавление ──")
a = [1, 2]
a.append(3)              # один элемент
a.extend([4, 5])         # несколько элементов
a.insert(0, 0)           # в начало — сдвиг всех элементов, O(n)
print(a)

# ── 05. Удаление ───────────────────────────────────────────────────────────
print("\n── 05. Удаление ──")
a = [10, 20, 30, 20]
print(a.pop())            # последний элемент
print(a.pop(0))           # по индексу
print(a.remove(30))       # None — remove ничего не возвращает
print(a)

# ── 06. Поиск ──────────────────────────────────────────────────────────────
print("\n── 06. Поиск ──")
tags = ["python", "sql", "python", "dbt"]
print(tags.index("sql"))       # позиция первого вхождения
print(tags.count("python"))    # сколько раз встречается
print("dbt" in tags)           # проверка входа O(n)
print("airflow" in tags)

# ── 07. Сортировка ─────────────────────────────────────────────────────────
print("\n── 07. Сортировка ──")
amounts = [1200, 800, 1500]
result = amounts.sort(reverse=True)
print(amounts)
print(result)                  # None — сортировка на месте

orders = [("Anna", 1200), ("Ivan", 800), ("Olga", 1500)]
orders.sort(key=lambda o: o[1])
print(orders)

# ── 08. Копия и алиас ──────────────────────────────────────────────────────
print("\n── 08. Копия и алиас ──")
a = [1, 2]
alias = a
copy = a.copy()           # то же самое: a[:] или list(a)
alias.append(3)
print(a, copy)
copy.append(4)
print(a, copy)

nested = [[1], [2]]
shallow = nested.copy()
shallow[0].append(99)
print(nested)             # вложенные объекты общие — это поверхностная копия

# ── 09. Срезы ──────────────────────────────────────────────────────────────
print("\n── 09. Срезы ──")
a = [10, 20, 30, 40, 50]
print(a[:2])        # копия первых двух
print(a[1:4])
print(a[::2])       # каждый второй
print(a[::-1])      # разворот
a[1:3] = [0]        # замена куска
print(a)
del a[1]            # del по индексу
print(a)

# ── 10. Операторы и встроенные функции ────────────────────────────────────
print("\n── 10. Операторы ──")
a = [1, 2]
print(a + [3])           # новый список
print(a * 2)
print(sum(a), min(a), max(a), len(a))

# ── 11. Сценарий: стек ─────────────────────────────────────────────────────
print("\n── 11. Сценарий: стек ──")
def is_balanced(text):
    stack = []
    pairs = {")": "(", "]": "["}
    for ch in text:
        if ch in "([":
            stack.append(ch)
        elif ch in ")]":
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

print(is_balanced("([[]])"))
print(is_balanced("([)]"))

# ── 12. Сценарий: топ-N ────────────────────────────────────────────────────
print("\n── 12. Сценарий: топ-N ──")
orders = [("Anna", 1200), ("Ivan", 800), ("Olga", 1500), ("Anna", 500), ("Olga", 300)]
totals = {}
for user, amount in orders:
    totals[user] = totals.get(user, 0) + amount

top3 = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:3]
print(top3)

# ── 13. Сценарий: батчи ────────────────────────────────────────────────────
print("\n── 13. Сценарий: батчи ──")
def chunks(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]

print(chunks([1, 2, 3, 4, 5], 2))
