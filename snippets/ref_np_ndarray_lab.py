# -*- coding: utf-8 -*-
"""Справочник: ndarray. Все примеры страницы ref-np-ndarray.html.

Требуется numpy 2.3.5 (как в книге).
Запуск из корня проекта:
    python3 guide/snippets/ref_np_ndarray_lab.py

Вывод детерминирован: random идёт через default_rng(seed), без времени и id.
"""

import numpy as np


def block(title):
    """Маркер раздела — как в остальных лабораториях книги."""
    print(f"\n── {title} ──")


# ── 03. Как создать ────────────────────────────────────────────────────────
block("03. Как создать")
arr = np.array([1200, 800, 1500, 500])
grid = np.array([[1, 2, 3], [4, 5, 6]])
texts = np.array(["Anna", "Olga", "Ivan"])
print(arr)
print(grid)
print(texts, texts.dtype)


# ── 05.1 Паспорт массива ───────────────────────────────────────────────────
block("05.1 Паспорт массива")
arr = np.array([1200, 800, 1500, 500])
grid = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape, arr.ndim, arr.size)
print(arr.dtype, arr.itemsize)
print(grid.shape, grid.ndim, grid.size)
print(grid.nbytes, grid.strides)
print(grid.flags["C_CONTIGUOUS"])


# ── 05.2 Память: nbytes и getsizeof ────────────────────────────────────────
block("05.2 Память: nbytes и getsizeof")
import sys

arr = np.zeros(1000, dtype=np.int64)
print(arr.nbytes, arr.itemsize * arr.size)
print(sys.getsizeof(arr))
print(np.zeros(1000, dtype=np.float32).nbytes)
print(np.array([1200, 800]).nbytes)


# ── 05.3 Создание генераторами ─────────────────────────────────────────────
block("05.3 Создание генераторами")
print(np.zeros((2, 3), dtype=np.int8))
print(np.ones(4))
print(np.full((2, 2), 7))
print(np.arange(0, 10, 3))
print(np.linspace(0, 1, 5))
print(np.eye(3, dtype=np.int8))


# ── 05.4 Random с seed ─────────────────────────────────────────────────────
block("05.4 Random с seed")
rng = np.random.default_rng(0)
print(rng.integers(0, 10, size=5))
print(rng.random(3).round(2))


# ── 05.5 dtype, astype и переполнение ──────────────────────────────────────
block("05.5 dtype, astype и переполнение")
mixed = np.array([1, 2.5])
print(mixed, mixed.dtype)

arr = np.array([1, 2, 3])
print(arr.astype(np.float32), arr.astype(np.float32).dtype)
print(np.array([200]).astype(np.int8))
print(np.array([127], dtype=np.int8) + 1)
print(np.array([0.1, 0.2, 0.3]).sum())


# ── 05.6 array, asarray и ошибки создания ──────────────────────────────────
block("05.6 array, asarray и ошибки создания")
arr = np.array([1200, 800, 1500, 500])
print(np.asarray(arr) is arr)
print(np.array(arr) is arr)

copy = np.array(arr)
copy[0] = 99
print(arr)
print(copy)

try:
    np.array([1, 2, 3], copy=False)
except ValueError as e:
    print(type(e).__name__, str(e).splitlines()[0])

try:
    np.array([[1, 2], [3]])
except ValueError as e:
    print(type(e).__name__, str(e).split(".")[0])


# ── 05.7 list против ndarray ───────────────────────────────────────────────
block("05.7 list против ndarray")
amounts = [1200, 800, 1500]
print(amounts + [500])
print([x * 2 for x in amounts])
print(np.array(amounts) * 2)
print(np.array(amounts) / 2)
try:
    print(amounts + 1)
except TypeError as e:
    print(type(e).__name__, e)


# ── 05.8 reshape, ravel, T, copy ───────────────────────────────────────────
block("05.8 reshape, ravel, T, copy")
grid = np.array([[1, 2, 3], [4, 5, 6]])
print(grid.reshape(6))
print(grid.reshape(3, 2).shape)
print(grid.ravel())
print(grid.T)
print(grid.T.shape)
print(grid.copy().shape)


# ── 06.1 Сценарий: скидка на все заказы ────────────────────────────────────
block("06.1 Сценарий: скидка на все заказы")
amounts = np.array([1200, 800, 1500, 500, 300])
discounted = amounts * 9 // 10
print(discounted)
print(discounted.sum(), amounts.sum())


# ── 06.2 Сценарий: нормализация оценок ─────────────────────────────────────
block("06.2 Сценарий: нормализация оценок")
scores = np.array([68.0, 92.0, 81.0, 55.0])
norm = (scores - scores.min()) / (scores.max() - scores.min())
print(norm.round(2))


# ── 06.3 Сценарий: float32 экономит память ─────────────────────────────────
block("06.3 Сценарий: float32 экономит память")
prices = np.array([1200, 800, 1500, 500], dtype=np.int64)
print(prices.nbytes)
print(prices.astype(np.float32).nbytes)
print(prices.astype(np.float32))


# ── 08.1 Решение: паспорт датасета ─────────────────────────────────────────
block("08.1 Решение: паспорт датасета")
orders = np.array([[1200, 800, 1500],
                   [500, 300, 900]])
print(orders.shape, orders.size, orders.nbytes, orders.dtype)


# ── 08.2 Решение: скидка и сумма ───────────────────────────────────────────
block("08.2 Решение: скидка и сумма")
amounts = np.array([1200, 800, 1500])
discounted = amounts * 9 // 10
print(discounted, discounted.sum())
