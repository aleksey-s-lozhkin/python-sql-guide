"""Лаборатория к главе 06: Counter, defaultdict, deque.

Запуск:  python3 guide/snippets/06_collections_lab.py
"""
import sys
import time
from collections import Counter, defaultdict, deque

print("Python", sys.version.split()[0])
print("=" * 64)

# ─── 1. Counter: частоты ──────────────────────────────────────────
print("\n1) COUNTER: СЧЁТЧИК С ТАБЛО")
words = ["sql", "python", "sql", "pandas", "python", "sql"]
counts = Counter(words)
print("   counts            :", dict(counts))
print("   most_common(2)    :", counts.most_common(2))
print("   counts['sql']     :", counts["sql"])
print("   counts['missing'] :", counts["missing"], " ← 0 без KeyError")
print("   'missing' in counts:", "missing" in counts, " ← но ключ не создан")
print("   total()           :", counts.total())

# ─── 2. Арифметика Counter ────────────────────────────────────────
print("\n2) АРИФМЕТИКА COUNTER — ОПЕРАЦИИ НАД МУЛЬТИМНОЖЕСТВАМИ")
a = Counter({"python": 3, "sql": 1})
b = Counter({"python": 1, "sql": 2})
print("   a + b →", dict(a + b))
print("   a - b →", dict(a - b), " ← нулевые и отрицательные исчезают")
print("   a & b →", dict(a & b), "  (минимум)")
print("   a | b →", dict(a | b), "  (максимум)")

# ─── 3. defaultdict: группировка ─────────────────────────────────
print("\n3) DEFAULTDICT: ГРУППИРОВКА БЕЗ ПРОВЕРОК")
orders = [
    {"user": "Anna", "amount": 1200},
    {"user": "Ivan", "amount": 800},
    {"user": "Anna", "amount": 500},
]
by_user = defaultdict(list)
for order in orders:
    by_user[order["user"]].append(order["amount"])
print("   dict(by_user) →", dict(by_user))

# ─── 4. Что делает чтение в defaultdict ───────────────────────────
print("\n4) ЧТЕНИЕ В DEFAULTDICT СОЗДАЁТ КЛЮЧ, GET — НЕТ")
d = defaultdict(int)
print("   d.get('x') →", d.get("x"), "| 'x' in d →", "x" in d)
print("   d['x']     →", d["x"], "| 'x' in d →", "x" in d)

# ─── 5. deque: оба конца ──────────────────────────────────────────
print("\n5) DEQUE: ОЧЕРЕДЬ С ДВУМЯ КОНЦАМИ")
q = deque([1, 2, 3])
q.appendleft(0)
q.append(4)
print("   deque       →", q)
print("   popleft()   →", q.popleft(), "| pop() →", q.pop())
print("   остаток     →", q)

# ─── 6. maxlen: скользящее окно ───────────────────────────────────
print("\n6) DEQUE(maxlen=N): АВТОМАТИЧЕСКОЕ СКОЛЬЗЯЩЕЕ ОКНО")
window = deque(maxlen=3)
for value in range(6):
    window.append(value)
    print("   добавили", value, "→", list(window))

# ─── 7. Почему deque, а не list для очереди ──────────────────────
print("\n7) ВСТАВКА В НАЧАЛО: LIST ПРОТИВ DEQUE")
n = 100_000

lst = []
t0 = time.perf_counter()
for i in range(n):
    lst.insert(0, i)
t_list = (time.perf_counter() - t0) * 1000

dq = deque()
t0 = time.perf_counter()
for i in range(n):
    dq.appendleft(i)
t_deque = (time.perf_counter() - t0) * 1000

print(f"   list.insert(0): {t_list:7.1f} ms")
print(f"   deque.appendleft: {t_deque:7.1f} ms")

# ─── 8. Counter на больших данных ─────────────────────────────────
print("\n8) COUNTER ПРОТИВ РУЧНОГО СЛОВАРЯ")
import random

random.seed(0)
data = [random.randint(1, 100) for _ in range(300_000)]

t0 = time.perf_counter()
manual = {}
for x in data:
    manual[x] = manual.get(x, 0) + 1
t_manual = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
fast = Counter(data)
t_counter = (time.perf_counter() - t0) * 1000

print(f"   dict.get: {t_manual:6.1f} ms")
print(f"   Counter : {t_counter:6.1f} ms")
print("   результаты совпали:", manual == dict(fast))
print("=" * 64)
