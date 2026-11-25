"""Лаборатория к главе 07: ndarray.

Запуск:  python3 guide/snippets/07_ndarray_lab.py
"""
import sys
import time

import numpy as np

print("Python", sys.version.split()[0], "| numpy", np.__version__)
print("=" * 64)

# ─── 1. Паспорт массива ───────────────────────────────────────────
print("\n1) ПАСПОРТ: shape, ndim, dtype, size")
ages = np.array([22, 31, 25, 40, 19])
print("   ages        :", ages)
print("   shape       :", ages.shape)
print("   ndim        :", ages.ndim)
print("   dtype       :", ages.dtype)
print("   size        :", ages.size)

grid = np.array([[1, 2, 3], [4, 5, 6]])
print("   grid.shape  :", grid.shape, "| ndim:", grid.ndim, "| size:", grid.size)
print("   strides     :", grid.strides, " байт на шаг по каждой оси")

# ─── 2. Память: список против массива ─────────────────────────────
print("\n2) ПАМЯТЬ: СПИСОК ССЫЛОК ПРОТИВ НЕПРЕРЫВНОГО БУФЕРА")
n = 1_000_000
plain = list(range(n))
arr = np.arange(n)
print(f"   list из {n:,}: {sys.getsizeof(plain):,} байт указателей + сами int-объекты")
print(f"   ndarray      : {arr.nbytes:,} байт данных, объект {sys.getsizeof(arr):,} байт")
print(f"   один Python int: {sys.getsizeof(123456)} байт; int64 в массиве: {arr.itemsize} байт")

# ─── 3. Скорость: создание и сумма ────────────────────────────────
print("\n3) СКОРОСТЬ: ЦИКЛ PYTHON ПРОТИВ ВЕКТОРНОЙ ОПЕРАЦИИ")
t0 = time.perf_counter()
squares_list = [i * i for i in range(n)]
t_list = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
squares_arr = np.arange(n) ** 2
t_arr = (time.perf_counter() - t0) * 1000

print(f"   создать: list {t_list:7.1f} ms | ndarray {t_arr:7.1f} ms")

t0 = time.perf_counter()
sum_list = sum(squares_list)
t_sum_list = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
sum_arr = int(squares_arr.sum())
t_sum_arr = (time.perf_counter() - t0) * 1000

print(f"   сложить: sum(list) {t_sum_list:6.1f} ms | .sum() {t_sum_arr:6.1f} ms")
print("   суммы совпали:", sum_list == sum_arr)

# ─── 4. dtype: тип задаётся один раз на весь массив ───────────────
print("\n4) DTYPE: ОДИН ТИП НА ВСЕ ЭЛЕМЕНТЫ")
print("   [1, 2, 3]        →", np.array([1, 2, 3]).dtype)
print("   [1, 2, 3.0]      →", np.array([1, 2, 3.0]).dtype)
print("   dtype=np.float32 →", np.array([1, 2, 3], dtype=np.float32).dtype)
print("   .astype(float)   →", np.array([1, 2, 3]).astype(float).dtype)
print("   itemsize int64   :", np.array([1]).itemsize, "байт")

# ─── 5. Переполнение int8 ─────────────────────────────────────────
print("\n5) ПЕРЕПОЛНЕНИЕ: INT8 НЕ РЕЗИНОВЫЙ")
tiny = np.array([127], dtype=np.int8)
with np.errstate(over="ignore"):
    print("   np.int8 127 + 1 →", (tiny + 1)[0])

# ─── 6. arange с float ────────────────────────────────────────────
print("\n6) ARANGE С FLOAT: ДЛИНА И ПОСЛЕДНИЙ ЭЛЕМЕНТ МОГУТ УДИВИТЬ")
x = np.arange(1, 1.3, 0.1)
print("   len(np.arange(1, 1.3, 0.1)) :", len(x))
print("   последний элемент           :", repr(x[-1]))
print("   последний == 1.3            :", x[-1] == 1.3)
print("   linspace(1, 1.3, 4)         :", np.linspace(1, 1.3, 4))

# ─── 7. np.array и np.asarray ────────────────────────────────────
print("\n7) ARRAY КОПИРУЕТ, ASARRAY МОЖЕТ НЕ КОПИРОВАТЬ")
original = np.array([1, 2, 3])
copy_arr = np.array(original)
same_arr = np.asarray(original)
print("   np.array(arr) is arr   →", copy_arr is original)
print("   np.asarray(arr) is arr →", same_arr is original)

# ─── 8. Создание массивов ─────────────────────────────────────────
print("\n8) БЫСТРОЕ СОЗДАНИЕ")
print("   zeros(3)        :", np.zeros(3))
print("   ones((2, 2))    :\n", np.ones((2, 2)))
print("   full((2, 2), 7) :\n", np.full((2, 2), 7))
print("   arange(0, 10, 3):", np.arange(0, 10, 3))
print("   linspace(0, 1, 5):", np.linspace(0, 1, 5))
print("   reshape 3×4:\n", np.arange(12).reshape(3, 4))

# ─── 9. Агрегаты ─────────────────────────────────────────────────
print("\n9) АГРЕГАТЫ БЕЗ ЦИКЛОВ")
print("   ages.mean() :", ages.mean())
print("   ages.max()  :", ages.max(), "| argmax:", ages.argmax())
print("   ages.min()  :", ages.min(), "| std:", round(float(ages.std()), 2))
print("=" * 64)
