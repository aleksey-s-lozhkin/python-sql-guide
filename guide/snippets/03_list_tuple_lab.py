"""Лаборатория к главе 03: list и tuple.

Запуск:  python3 guide/snippets/03_list_tuple_lab.py
Все выводы в главе получены этим файлом на Python 3.12.
"""
import sys
import time

print("Python", sys.version.split()[0])
print("=" * 64)

# ─── 1. Два имени одного поезда и копия состава ────────────────────
print("\n1) ПРИСВАИВАНИЕ — ЭТО ВТОРОЕ ИМЯ, СРЕЗ — НОВЫЙ СОСТАВ")
a = [1, 2, 3]
b = a          # b — второе имя того же объекта
c = a[:]       # c — новый список с теми же значениями
b.append(4)

print("   a =", a, "| c =", c)
print("   a is b →", a is b, "  a is c →", a is c)
print("   id(a)=%s id(b)=%s id(c)=%s" % (id(a), id(b), id(c)))

# ─── 2. Копия неглубокая: вложенные объекты общие ──────────────────
print("\n2) СРЕЗ КОПИРУЕТ СПИСОК, НО НЕ ЕГО СОДЕРЖИМОЕ")
matrix = [[1, 2], [3, 4]]
shallow = matrix[:]
shallow[0].append(99)
print("   matrix =", matrix, " ← изменился и исходный")
print("   matrix[0] is shallow[0] →", matrix[0] is shallow[0])

# ─── 3. Три ссылки на один список ──────────────────────────────────
print("\n3) [[0]] * 3 — ТРИ ИМЕНИ ОДНОГО ВАГОНА")
grid = [[0]] * 3
grid[0].append(1)
print("   grid =", grid)
print("   все элементы — один объект:", len({id(x) for x in grid}) == 1)
fresh = [[0] for _ in range(3)]
fresh[0].append(1)
print("   [[0] for _ in range(3)] →", fresh)

# ─── 4. Неизменяемость tuple и хеш ─────────────────────────────────
print("\n4) TUPLE: НЕЛЬЗЯ ПЕРЕСТАВИТЬ ГРУЗ, ЗАТО МОЖНО ОПЕЧАТАТЬ")
point = (10, 20)
try:
    point[0] = 99
except TypeError as e:
    print("   point[0] = 99 → TypeError:", e)

print("   hash((10, 20)) =", hash((10, 20)))
order = ("anna", "2024-05-01")
print("   dict с tuple-ключом:", {order: 1200})

try:
    {("anna", ["IT"]): 1200}
except TypeError as e:
    print("   tuple с list внутри → TypeError:", e)

# ─── 5. Неизменяемость неглубокая ──────────────────────────────────
print("\n5) TUPLE ЗАЩИЩАЕТ ССЫЛКИ, А НЕ СОДЕРЖИМОЕ")
box = (1, [2, 3])
box[1].append(4)
print("   box =", box, " ← список внутри изменился")

# ─── 6. append против insert(0) ────────────────────────────────────
print("\n6) append O(1) ПРОТИВ insert(0) O(n)")
n = 100_000
tail = []
t0 = time.perf_counter()
for i in range(n):
    tail.append(i)
t_append = (time.perf_counter() - t0) * 1000

head = []
t0 = time.perf_counter()
for i in range(n):
    head.insert(0, i)
t_insert = (time.perf_counter() - t0) * 1000

print(f"   append:    {t_append:7.1f} ms")
print(f"   insert(0): {t_insert:7.1f} ms")
print(f"   разница ≈ {t_insert / t_append:.0f}x")

# ─── 7. sort() меняет на месте, sorted() возвращает новый ──────────
print("\n7) sort() ВОЗВРАЩАЕТ None")
nums = [3, 1, 2]
result = nums.sort()
print("   result =", result, "| nums =", nums)
print("   sorted(nums) =", sorted(nums), "| nums =", nums)

# ─── 8. += для list и для tuple — разные вещи ──────────────────────
print("\n8) += : ДЛЯ LIST ЭТО МУТАЦИЯ, ДЛЯ TUPLE — ПЕРЕСБОРКА")


def add_room_list(rooms, room):
    rooms += [room]          # in-place: меняет список вызывающего


def add_room_tuple(rooms, room):
    rooms += (room,)         # новая привязка: вызывающий не видит изменений


my_list = ["kitchen"]
add_room_list(my_list, "hall")
print("   list после += →", my_list)

my_tuple = ("kitchen",)
add_room_tuple(my_tuple, "hall")
print("   tuple после += →", my_tuple)

# ─── 9. Ловушка изменяемого аргумента по умолчанию ─────────────────
print("\n9) АРГУМЕНТ ПО УМОЛЧАНИЮ ЖИВЁТ МЕЖДУ ВЫЗОВАМИ")


def append_bad(item, acc=[]):
    acc.append(item)
    return acc


print("   append_bad(1) →", append_bad(1))
print("   append_bad(2) →", append_bad(2))


def append_ok(item, acc=None):
    if acc is None:
        acc = []
    acc.append(item)
    return acc


print("   append_ok(1)  →", append_ok(1))
print("   append_ok(2)  →", append_ok(2))

# ─── 10. Память и создание: tuple дешевле ──────────────────────────
print("\n10) TUPLE КОМПАКТНЕЕ И БЫСТРЕЕ В СОЗДАНИИ")
small_list = [10, 20, 30]
small_tuple = (10, 20, 30)
print("   sys.getsizeof([10,20,30]) =", sys.getsizeof(small_list))
print("   sys.getsizeof((10,20,30))  =", sys.getsizeof(small_tuple))

n = 2_000_000
t0 = time.perf_counter()
_ = [tuple(range(3)) for _ in range(n)]
t_tuple = time.perf_counter() - t0
t0 = time.perf_counter()
_ = [list(range(3)) for _ in range(n)]
t_list = time.perf_counter() - t0
print(f"   создать {n:,} tuple: {t_tuple * 1000:.0f} ms")
print(f"   создать {n:,} list:  {t_list * 1000:.0f} ms")

# ─── 11. Распаковка и срезы ───────────────────────────────────────
print("\n11) РАСПАКОВКА И СРЕЗЫ")
first, *middle, last = [1, 2, 3, 4, 5]
print("   first, *middle, last →", first, middle, last)
print("   [1,2,3,4,5][::-1] →", [1, 2, 3, 4, 5][::-1])
print("   [1,2,3,4,5][1:4:2] →", [1, 2, 3, 4, 5][1:4:2])
print("=" * 64)
