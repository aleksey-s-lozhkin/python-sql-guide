"""Лаборатория к главе 2: dict — это шкаф с номерками.

Запуск:  python3 01_dict_lab.py
Всё, что печатается здесь, воспроизводится у тебя на машине
(кроме настоящих hash() — они рандомизированы между запусками).
"""
import sys
import time

print("Python", sys.version.split()[0])
print("=" * 62)

# ─── 1. Хеш — это номерок на пальто ────────────────────────────────
print("\n1) НАСТОЯЩИЙ hash(): у каждого запуска свой результат")
print("   hash('anna') =", hash("anna"), "  ← у тебя будет другое число")
print("   Это защита от подбора коллизий (PYTHONHASHSEED).")

# ─── 2. Игрушечная хеш-таблица: видно, как это работает ────────────
print("\n2) ИГРУШЕЧНЫЙ хеш: sum(ord(c)) % 8 — детерминированно")

BUCKETS = 8


def toy_hash(key: str) -> int:
    """Складываем коды символов и берём остаток — как «номер вешалки»."""
    return sum(map(ord, key)) % BUCKETS


names = ["anna", "ivan", "petr", "olga", "max", "lena", "oleg", "vera"]
for n in names:
    print(f"   {n:5} → hash={sum(map(ord, n)):4}  → ячейка {toy_hash(n)}")

# Коллизия: два разных ключа попали в одну ячейку.
seen: dict[int, str] = {}
collisions = []
for n in names:
    b = toy_hash(n)
    if b in seen:
        collisions.append((seen[b], n, b))
    else:
        seen[b] = n
print("   Коллизии (разные ключи — одна ячейка):", collisions or "нет в этом наборе")

# ─── 3. Почему list не годится в ключи ─────────────────────────────
print("\n3) HASHABLE = неизменяемый + __hash__ + __eq__")
try:
    d = {["anna"]: 1}
except TypeError as e:
    print("   {['anna']: 1} → TypeError:", e)

print("   tuple можно:", {("Ivan", "IT"): 42})
print("   tuple с list внутри нельзя:", end=" ")
try:
    {("Ivan", ["IT"]): 42}
except TypeError as e:
    print("TypeError:", e)

# ─── 4. Поиск: список O(n) против dict O(1) ────────────────────────
print("\n4) ПОИСК: list просматривает всё, dict прыгает в ячейку")
users = [f"user{i}" for i in range(1_000_000)]
by_name = {u: i for i, u in enumerate(users)}

t0 = time.perf_counter()
"user999999" in users
t_list = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
"user999999" in by_name
t_dict = (time.perf_counter() - t0) * 1_000_000

print(f"   list: {t_list:8.2f} ms")
print(f"   dict: {t_dict:8.2f} µs")
print(f"   ускорение ≈ {t_list / (t_dict / 1000):.0f}x")

# ─── 5. get, setdefault, += 1 и типичная ловушка ───────────────────
print("\n5) ЧТЕНИЕ И ОБНОВЛЕНИЕ")
order = {"user": "Anna", "amount": 1200}
print("   order.get('city')      →", order.get("city"))
print("   order.get('city', '—') →", order.get("city", "—"))
print("   order.setdefault('currency', 'RUB') →", order.setdefault("currency", "RUB"))
print("   'city' in order        →", "city" in order)

try:
    order["city"] += " Москва"  # KeyError: ключа ещё нет
except KeyError as e:
    print("   order['city'] += ...   → KeyError:", e)

# ─── 6. Порядок вставки сохраняется (Python 3.7+) ──────────────────
print("\n6) ПОРЯДОК: dict помнит порядок вставки, но это не сортировка")
d = {"b": 2, "a": 1}
d["c"] = 3
print("   ", dict(d), "| sorted по ключу:", dict(sorted(d.items())))

# ─── 7. Мост в pandas: тот же «dict-аккумулятор» ───────────────────
print("\n7) МОСТ В PANDAS: groupby — это тот же словарь-аккумулятор")
try:
    import pandas as pd

    orders = pd.DataFrame(
        {
            "user": ["Anna", "Ivan", "Anna", "Petr"],
            "amount": [1200, 800, 500, 2100],
        }
    )
    print(orders.groupby("user")["amount"].sum().to_string())
except ImportError:
    print("   pandas не установлен — пропускаем")
print("=" * 62)
