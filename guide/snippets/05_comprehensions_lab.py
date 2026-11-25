"""Лаборатория к главе 05: comprehensions и генераторы.

Запуск:  python3 guide/snippets/05_comprehensions_lab.py
"""
import sys
import time

print("Python", sys.version.split()[0])
print("=" * 62)

# ─── 1. Одна идея в трёх записях ───────────────────────────────────
print("\n1) ОДНА ИДЕЯ: ЦИКЛ, COMPREHENSION, ГЕНЕРАТОР")
plain = []
for x in range(6):
    if x % 2 == 0:
        plain.append(x * x)

comp = [x * x for x in range(6) if x % 2 == 0]
gen = (x * x for x in range(6) if x % 2 == 0)

print("   цикл:        ", plain)
print("   comprehension:", comp)
print("   генератор:   ", gen, "→", list(gen))

# ─── 2. Dict и set comprehension ──────────────────────────────────
print("\n2) DICT И SET COMPREHENSION")
words = ["sql", "python", "pandas", "polars"]
print("   {w: len(w)}  :", {w: len(w) for w in words})
print("   {w[0] for w}:", {w[0] for w in words})

# ─── 3. Вложенные циклы: развернуть матрицу ────────────────────────
print("\n3) ВЛОЖЕННЫЙ ЦИКЛ В COMPREHENSION")
matrix = [[1, 2], [3, 4], [5, 6]]
print("   [x for row in matrix for x in row] →", [x for row in matrix for x in row])
print("   [(i, j) для пар] →", [(i, j) for i in range(2) for j in range(2)])

# ─── 4. Память: список против генератора ──────────────────────────
print("\n4) ПАМЯТЬ: СПИСОК ПРОТИВ ГЕНЕРАТОРА")
n = 1_000_000
lst = [x * x for x in range(n)]
gen = (x * x for x in range(n))
print(f"   список из {n:,}: {sys.getsizeof(lst):,} байт")
print(f"   генератор     : {sys.getsizeof(gen):,} байт")

# ─── 5. Один проход ───────────────────────────────────────────────
print("\n5) ГЕНЕРАТОР ИСЧЕРПЫВАЕТСЯ ЗА ОДИН ПРОХОД")
g = (x * x for x in range(5))
print("   sum(g) →", sum(g))
print("   sum(g) →", sum(g), " ← второй раз пусто")

# ─── 6. Первый элемент: список против генератора ──────────────────
print("\n6) ВРЕМЯ ДО ПЕРВОГО ЭЛЕМЕНТА")
t0 = time.perf_counter()
first_from_list = [x * x for x in range(n)][0]
t_list = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
first_from_gen = next(x * x for x in range(n))
t_gen = (time.perf_counter() - t0) * 1_000_000

print(f"   список:   {t_list:7.2f} ms (построить всё)")
print(f"   генератор:{t_gen:7.2f} µs (только первый)")
print("   значения:", first_from_list, first_from_gen)

# ─── 7. yield: генераторная функция ───────────────────────────────
print("\n7) ГЕНЕРАТОРНАЯ ФУНКЦИЯ С yield")


def squares(limit):
    for i in range(limit):
        yield i * i


print("   list(squares(5)) →", list(squares(5)))
print("   sum(squares(5))  →", sum(squares(5)))

# ─── 8. Ленивость и короткое замыкание ────────────────────────────
print("\n8) ЛЕНИВОСТЬ: ПРОВЕРКА ОСТАНАВЛИВАЕТСЯ НА ПЕРВОМ СОВПАДЕНИИ")
big = range(10_000_000)

t0 = time.perf_counter()
has_big = any(x > 5 for x in big)
t_any = (time.perf_counter() - t0) * 1_000_000

t0 = time.perf_counter()
all_small = all(x < 5 for x in big)
t_all = (time.perf_counter() - t0) * 1_000_000

print(f"   any(x > 5) → {has_big} за {t_any:.1f} µs")
print(f"   all(x < 5) → {all_small} за {t_all:.1f} µs")
print("   диапазон 10 млн: оба вызова не прошли его целиком")

# ─── 9. Ловушка замыкания ─────────────────────────────────────────
print("\n9) LAMBDA В COMPREHENSION ЗАПОМИНАЕТ ПЕРЕМЕННУЮ, А НЕ ЗНАЧЕНИЕ")
funcs = [lambda: i for i in range(3)]
print("   [f() for f in funcs] →", [f() for f in funcs])

funcs_fixed = [lambda i=i: i for i in range(3)]
print("   с i=i              →", [f() for f in funcs_fixed])

# ─── 10. У генератора нет len() ───────────────────────────────────
print("\n10) У ГЕНЕРАТОРА НЕТ len()")
g2 = (x for x in range(10))
try:
    len(g2)
except TypeError as e:
    print("   len(g2) → TypeError:", e)
print("   количество: sum(1 for _ in g2) →", sum(1 for _ in g2))
print("=" * 62)
