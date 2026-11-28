"""Справочник NumPy: axis. Все примеры страницы ref-np-axis.html.

Требуется numpy 2.3.5 (как в книге).
Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_np_axis_lab.py

Вывод детерминирован: массивы маленькие, floats округлены там, где это
важно, поэтому repr не зависит от версии и ширины терминала.
"""

# ── 03. Подготовка: одна матрица ───────────────────────────────────────────
print("── 03. Подготовка ──")
import numpy as np

m = np.arange(12).reshape(3, 4)
print(m)
print(m.shape, m.ndim, m.dtype)

# ── 05.1. axis=0 и axis=1: две суммы ───────────────────────────────────────
print("\n── 05.1. Две суммы ──")
print(m.sum(axis=0), m.sum(axis=0).shape)
print(m.sum(axis=1), m.sum(axis=1).shape)
print(m.sum(), m.sum().shape)

# ── 05.2. mean, min, max, prod, std, var ───────────────────────────────────
print("\n── 05.2. Остальные агрегаты ──")
print(m.mean(axis=0))
print(m.mean(axis=1))
print(m.min(axis=0), m.max(axis=0))
print(m.prod(axis=1))
print(m.std(axis=0).round(2))
print(m.var(axis=1).round(2))

# ── 05.3. keepdims, отрицательная ось и axis=(0, 1) ────────────────────────
print("\n── 05.3. keepdims и несколько осей ──")
print(m.sum(axis=0).shape, m.sum(axis=0, keepdims=True).shape)
print(m.sum(axis=0, keepdims=True))
print(np.array_equal(m.sum(axis=-1), m.sum(axis=1)))
print(m.sum(axis=(0, 1)), m.sum(axis=(0, 1)).shape)
print(m.sum(axis=(0, 1), keepdims=True))

# ── 05.4. any/all и булева маска ───────────────────────────────────────────
print("\n── 05.4. any/all ──")
mask = m > 5
print(mask)
print(mask.any(axis=0))
print(mask.all(axis=1))
print(mask.sum(axis=0))

# ── 05.5. argmax, argmin, cumsum, sort ─────────────────────────────────────
print("\n── 05.5. argmax, cumsum, sort ──")
print(m.argmax(), m.argmax(axis=0), m.argmax(axis=1))
print(m.argmin(axis=1))
print(m.cumsum(axis=0))
s = np.array([[3, 1], [0, 2]])
print(np.sort(s, axis=0))
print(np.sort(s, axis=1))

# ── 05.6. Трёхмерный массив (2, 3, 4) ──────────────────────────────────────
print("\n── 05.6. Трёхмерный массив ──")
cube = np.arange(24).reshape(2, 3, 4)
print(cube.shape)
print(cube.sum(axis=0).shape, cube.sum(axis=1).shape, cube.sum(axis=2).shape)
print(cube.sum(axis=(0, 2)))
print(cube.sum(axis=(0, 1)).shape, cube.sum(axis=(0, 1)))

# ── 06.1. Сценарий: выручка по дням и категориям ───────────────────────────
print("\n── 06.1. Сценарий: выручка по дням ──")
sales = np.array([
    [100, 200, 150, 50],
    [120, 180, 160, 40],
    [80, 220, 140, 60],
])
print(sales.sum(axis=0))
print(sales.sum(axis=1))
print(sales.mean(axis=0).round(1))

# ── 06.2. Сценарий: доли по дням через keepdims ────────────────────────────
print("\n── 06.2. Сценарий: доли по дням ──")
day_totals = sales.sum(axis=1, keepdims=True)
shares = (sales / day_totals * 100).round(1)
print(day_totals.shape, shares.shape)
print(shares)

# ── 06.3. Сценарий: 3D — партии, магазины, месяцы ──────────────────────────
print("\n── 06.3. Сценарий: 3D ──")
cube = np.arange(24).reshape(2, 3, 4) + 1
print(cube.shape)
print(cube.sum(axis=0).shape)
print(cube.sum(axis=0))
print(cube.sum(axis=(0, 2)))

# ── 07. Проверка ошибок ────────────────────────────────────────────────────
print("\n── 07. Проверка ошибок ──")
try:
    m.sum(axis=2)
except Exception as e:
    print(type(e).__name__, ":", e)
try:
    np.array(5).sum(axis=1)
except Exception as e:
    print(type(e).__name__, ":", e)
print("скаляр, axis=0:", np.array(5).sum(axis=0))
print("mean dtype:", m.mean(axis=0).dtype)
print("argmax без оси:", int(m.argmax()),
      tuple(int(i) for i in np.unravel_index(m.argmax(), m.shape)))
try:
    m - m.mean(axis=1)
except ValueError as e:
    print(type(e).__name__, ":", e)

# ── 08a. Задача: итоги матрицы 4×3 ─────────────────────────────────────────
print("\n── 08a. Задача: итоги 4×3 ──")
s = np.arange(12).reshape(4, 3)
print(s.sum(axis=0), s.sum(axis=1))
print(s.max(axis=0), s.argmax(axis=1))

# ── 08b. Задача: вычесть среднее по строкам ────────────────────────────────
print("\n── 08b. Задача: центрирование по строкам ──")
x = np.arange(12.0).reshape(3, 4)
row_means = x.mean(axis=1, keepdims=True)
centered = x - row_means
print(row_means.shape, centered.shape)
print(centered.mean(axis=1).round(10))
