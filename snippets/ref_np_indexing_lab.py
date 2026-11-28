# -*- coding: utf-8 -*-
"""Справочник: индексация ndarray. Все примеры страницы ref-np-indexing.html.

Требуется numpy 2.3.5 (как в книге).
Запуск из корня проекта:
    python3 guide/snippets/ref_np_indexing_lab.py

Вывод детерминирован: без времени, hash и id.
"""

import numpy as np


def block(title):
    """Маркер раздела — как в остальных лабораториях книги."""
    print(f"\n── {title} ──")


# ── 03. Как взять кусок ────────────────────────────────────────────────────
block("03. Как взять кусок")
ages = np.array([22, 31, 25, 40, 19])
grid = np.array([[1, 2, 3], [4, 5, 6]])
print(ages[1:4])
print(ages[ages > 25])
print(ages[[0, 2]])
print(grid[0, 1])


# ── 05.1 Базовые срезы и view ──────────────────────────────────────────────
block("05.1 Базовые срезы и view")
ages = np.array([22, 31, 25, 40, 19])
print(ages[1:4])
print(ages[-2:])
print(ages[::-1])
print(ages[::2])

grid = np.array([[1, 2, 3], [4, 5, 6]])
print(grid[0])
print(grid[:, 1])
print(grid[1:, ::2])

window = ages[1:4]
window[0] = 99
print(ages)


# ── 05.2 Маски ────────────────────────────────────────────────────────────
block("05.2 Маски")
ages = np.array([22, 31, 25, 40, 19])
mask = ages > 25
print(mask, mask.dtype)
print(ages[mask])

salaries = np.array([50000, 90000, 70000, 120000, 45000])
both = (ages > 25) & (salaries > 60000)
print(both)
print(ages[both])

print(ages[(ages < 25) | (ages > 35)])
print(ages[~(ages > 25)])


# ── 05.3 np.where ─────────────────────────────────────────────────────────
block("05.3 np.where")
ages = np.array([22, 31, 25, 40, 19])
print(np.where(ages > 25, "adult", "young"))
print(np.where(ages > 25, 1, 0))
print(np.where(ages > 25))

low = np.array([1, 2, 3, 4, 5])
high = np.array([10, 20, 30, 40, 50])
print(np.where(ages > 25, high, low))


# ── 05.4 Fancy indexing — копия ────────────────────────────────────────────
block("05.4 Fancy indexing — копия")
ages = np.array([22, 31, 25, 40, 19])
picked = ages[[0, 2, 4]]
print(picked)

picked[0] = 99
print(ages)
print(picked)

grid = np.array([[1, 2, 3], [4, 5, 6]])
print(grid[[1, 0]])
print(grid[[0, 1], [2, 0]])


# ── 05.5 take, clip, nonzero, argwhere ─────────────────────────────────────
block("05.5 take, clip, nonzero, argwhere")
ages = np.array([22, 31, 25, 40, 19])
print(np.take(ages, [4, 0]))
print(np.clip(ages, 25, 35))
print(np.nonzero(ages > 25))
print(np.argwhere(ages > 25))


# ── 05.6 Ошибки индексации ────────────────────────────────────────────────
block("05.6 Ошибки индексации")
ages = np.array([22, 31, 25, 40, 19])
try:
    ages[np.array([True, False])]
except IndexError as e:
    print(type(e).__name__, str(e).split(";")[0])

try:
    (ages > 25) and (ages < 35)
except ValueError as e:
    print(type(e).__name__, str(e).split(".")[0])

print(ages[[]], ages[[]].shape)
ages[[]] = 999
print(ages)


# ── 06.1 Сценарий: заказы дороже 1000 ──────────────────────────────────────
block("06.1 Сценарий: заказы дороже 1000")
users = np.array(["Anna", "Olga", "Ivan", "Anna", "Olga"])
amounts = np.array([1200, 800, 1500, 500, 300])
mask = amounts > 1000
print(users[mask])
print(amounts[mask].sum())
print(np.where(mask, amounts, 0))


# ── 06.2 Сценарий: два условия ────────────────────────────────────────────
block("06.2 Сценарий: два условия")
ages = np.array([22, 31, 25, 40, 19])
salaries = np.array([50000, 90000, 70000, 120000, 45000])
mask = (ages > 25) & (salaries > 60000)
print(mask)
print(ages[mask], salaries[mask])


# ── 06.3 Сценарий: категории через where ──────────────────────────────────
block("06.3 Сценарий: категории через where")
scores = np.array([68, 92, 81, 55])
labels = np.where(scores >= 80, "high", "low")
print(labels)
print(np.where(scores >= 80, scores, 0))


# ── 08.1 Решение: чётные числа ────────────────────────────────────────────
block("08.1 Решение: чётные числа")
nums = np.array([3, 8, 12, 5, 7, 10])
mask = nums % 2 == 0
print(nums[mask], nums[mask].sum())


# ── 08.2 Решение: порог через where ───────────────────────────────────────
block("08.2 Решение: порог через where")
temps = np.array([12, 25, 8, 30])
print(np.where(temps >= 20, "hot", "cold"))
