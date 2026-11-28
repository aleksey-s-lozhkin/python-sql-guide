"""Лаборатория к главе 04: set.

Запуск:  python3 guide/snippets/04_set_lab.py
"""
import sys
import time

print("Python", sys.version.split()[0])
print("=" * 62)

# ─── 1. Уникальность и потеря порядка ──────────────────────────────
print("\n1) SET УБИРАЕТ ДУБЛИ, НО НЕ ХРАНИТ ПОРЯДОК")
tags = ["sql", "python", "sql", "pandas", "python"]
print("   исходный список:", tags)
print("   set(tags)       :", set(tags))
print("   dict.fromkeys   :", list(dict.fromkeys(tags)), " ← порядок сохранён")
print("   set([3, 1, 2])  :", set([3, 1, 2]), " ← порядок вставки не сохраняется")

# ─── 2. Проверка входа: список против множества ────────────────────
print("\n2) IN: СПИСОК O(n) ПРОТИВ МНОЖЕСТВА O(1)")
users = [f"user{i}" for i in range(200_000)]
user_set = set(users)
needle = "user199999"

t0 = time.perf_counter()
needle in users
t_list = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
needle in user_set
t_set = (time.perf_counter() - t0) * 1_000_000

print(f"   list: {t_list:.2f} ms")
print(f"   set:  {t_set:.2f} µs")

# ─── 3. Четыре операции над множествами ───────────────────────────
print("\n3) ПЕРЕСЕЧЕНИЕ, ОБЪЕДИНЕНИЕ, РАЗНОСТЬ, СИММЕТРИЧЕСКАЯ РАЗНОСТЬ")
a = {"python", "sql", "pandas"}
b = {"python", "airflow", "dbt"}
print("   a & b →", sorted(a & b), "  (было там и там)")
print("   a | b →", sorted(a | b), "  (было хоть где-то)")
print("   a - b →", sorted(a - b), "  (только у a)")
print("   b - a →", sorted(b - a), "  (только у b)")
print("   a ^ b →", sorted(a ^ b), "  (ровно в одном)")

# ─── 4. Подмножества ───────────────────────────────────────────────
print("\n4) ПОДМНОЖЕСТВА И НЕПЕРЕСЕЧЕНИЕ")
print("   {'python'} <= a →", {"python"} <= a)
print("   a <= a          →", a <= a)
print("   {'java'} <= a   →", {"java"} <= a)
print("   a.isdisjoint({'java'}) →", a.isdisjoint({"java"}))

# ─── 5. Что можно класть в set ────────────────────────────────────
print("\n5) В SET МОЖНО ТОЛЬКО HASHABLE")
edges = {(1, 2), (2, 3), (1, 2), (3, 4)}
print("   set из tuple:", edges)
try:
    {["a", "b"]}
except TypeError as e:
    print("   set из list → TypeError:", e)

# ─── 6. frozenset как ключ словаря ────────────────────────────────
print("\n6) FROZENSET — НЕИЗМЕНЯЕМОЕ МНОЖЕСТВО, ГОДИТСЯ В КЛЮЧИ")
permissions = {frozenset({"read", "write"}): "editor",
               frozenset({"read"}): "viewer"}
print("   ключ из двух прав:", permissions[frozenset({"write", "read"})])

# ─── 7. Set comprehension ─────────────────────────────────────────
print("\n7) SET COMPREHENSION")
words = ["sql", "python", "pandas", "polars"]
print("   первые буквы:", {w[0] for w in words})
print("   длины ≥ 5   :", {len(w) for w in words if len(w) >= 5})

# ─── 8. Пересечение «в лоб» и через set ───────────────────────────
print("\n8) ПЕРЕСЕЧЕНИЕ: ВЛОЖЕННЫЙ ЦИКЛ ПРОТИВ SET")
left = [f"id{i}" for i in range(2_000)]
right = [f"id{i}" for i in range(1_000, 3_000)]

t0 = time.perf_counter()
naive = [x for x in left if x in right]
t_naive = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
fast = set(left) & set(right)
t_fast = (time.perf_counter() - t0) * 1000

print(f"   список: {t_naive:6.2f} ms, найдено {len(naive)}")
print(f"   set:    {t_fast:6.2f} ms, найдено {len(fast)}")

# ─── 9. Память ────────────────────────────────────────────────────
print("\n9) ПАМЯТЬ: SET ТЯЖЕЛЕЕ СПИСКА")
print("   list [1, 2, 3]      :", sys.getsizeof([1, 2, 3]), "байт")
print("   set {1, 2, 3}       :", sys.getsizeof({1, 2, 3}), "байт")
print("   frozenset {1, 2, 3} :", sys.getsizeof(frozenset({1, 2, 3})), "байт")
print("=" * 62)
