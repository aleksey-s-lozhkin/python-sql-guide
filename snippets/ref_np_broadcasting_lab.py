"""Справочник NumPy: broadcasting. Все примеры страницы ref-np-broadcasting.html.

Требуется numpy 2.3.5 (как в книге).
Запуск из корня проекта:
    /tmp/ref-pd-venv/bin/python guide/snippets/ref_np_broadcasting_lab.py

Вывод детерминирован: массивы маленькие, floats округлены там, где это
важно, поэтому repr не зависит от версии и ширины терминала.
"""

# ── 03. Подготовка: матрица, строка и столбец ──────────────────────────────
print("── 03. Подготовка ──")
import numpy as np

a = np.arange(12).reshape(3, 4)
row = np.array([10, 20, 30, 40])
col = np.array([[100], [200], [300]])
print(a)
print(a.shape, row.shape, col.shape)

# ── 05.1. Скаляр и строка (4,) ─────────────────────────────────────────────
print("\n── 05.1. Скаляр и строка ──")
print((a + 10).shape)
print(a + 10)
print(row.shape, (a + row).shape)
print(a + row)

# ── 05.2. Столбец (3, 1) прибавляется к каждому столбцу ────────────────────
print("\n── 05.2. Столбец (3, 1) ──")
print(col.shape, (a + col).shape)
print(a + col)

# ── 05.3. (3, 1) + (1, 4) → (3, 4) ─────────────────────────────────────────
print("\n── 05.3. (3, 1) + (1, 4) ──")
ones_col = np.ones((3, 1))
ones_row = np.ones((1, 4))
print((ones_col + ones_row).shape)
print(ones_col + ones_row)
print((col + row).shape)
print(col + row)

# ── 05.4. newaxis: вектор → столбец и строка ───────────────────────────────
print("\n── 05.4. newaxis ──")
v = np.array([1, 2, 3])
print(v.shape, v[:, None].shape, v[None, :].shape)
print(v[:, None] * v[None, :])

# ── 05.5. broadcast_to и broadcast_arrays: view без копирования ─────────────
print("\n── 05.5. view без копирования ──")
base = np.array([1, 2, 3])
big = np.broadcast_to(base, (2, 3))
print(big)
print(big.shape, big.strides, big.flags.writeable)
print(big.base is base, np.shares_memory(big, base))
try:
    big[0, 0] = 9
except ValueError as e:
    print(type(e).__name__, e)

x = np.array([[1], [2]])
y = np.array([10, 20, 30])
xs, ys = np.broadcast_arrays(x, y)
print(xs.shape, ys.shape)
print(xs.strides, ys.strides)
print(xs)
print(ys)

# ── 05.6. Несовместимые формы ──────────────────────────────────────────────
print("\n── 05.6. Несовместимые формы ──")
try:
    a + np.array([1, 2, 3])
except ValueError as e:
    print(type(e).__name__, e)
fixed = np.array([1, 2, 3])[:, None]
print(fixed.shape, (a + fixed).shape)
print(a + fixed)

# ── 05.7. Центрирование: keepdims + broadcasting ───────────────────────────
print("\n── 05.7. Центрирование ──")
col_means = a.mean(axis=0, keepdims=True)
centered = a - col_means
print(col_means.shape, centered.shape)
print(centered.mean(axis=0))

# ── 06.1. Сценарий: нормализация по столбцам ───────────────────────────────
print("\n── 06.1. Сценарий: нормализация ──")
x = np.arange(12, dtype=float).reshape(3, 4)
z = (x - x.mean(axis=0, keepdims=True)) / x.std(axis=0, keepdims=True)
print(z.round(2))
print(z.mean(axis=0).round(10))

# ── 06.2. Сценарий: матрица попарных разностей ─────────────────────────────
print("\n── 06.2. Сценарий: попарные разности ──")
v = np.array([10, 20, 35, 50])
diff = v[:, None] - v[None, :]
print(diff.shape)
print(diff[1])

# ── 06.3. Сценарий: скидка по категориям и наценка по магазинам ────────────
print("\n── 06.3. Сценарий: скидки и наценки ──")
amounts = np.array([[100, 200, 300], [150, 250, 350]])
discount = np.array([0.10, 0.20, 0.05])
markup = np.array([[1.5], [1.2]])
final = amounts * (1 - discount) * markup
print(final.round(1))

# ── 07. Проверка ошибок ────────────────────────────────────────────────────
print("\n── 07. Проверка ошибок ──")
try:
    a + np.array([1, 2, 3])
except ValueError as e:
    print(type(e).__name__, ":", e)
try:
    a - a.mean(axis=1)
except ValueError as e:
    print(type(e).__name__, ":", e)
r = np.ones((1, 4))
try:
    r += col
except ValueError as e:
    print(type(e).__name__, ":", e)
base = np.array([1, 2, 3])
big = np.broadcast_to(base, (2, 3))
print("writeable:", big.flags.writeable, "| base is base:", big.base is base)
copy = big.copy()
copy[0, 0] = 9
print("после copy:", copy[0, 0], "| base:", base[0])

# ── 08a. Задача: доли по строкам ───────────────────────────────────────────
print("\n── 08a. Задача: доли по строкам ──")
counts = np.array([
    [2, 3, 5, 0],
    [1, 1, 2, 6],
    [4, 0, 1, 5],
])
shares = (counts / counts.sum(axis=1, keepdims=True) * 100).round(1)
print(counts.sum(axis=1, keepdims=True).shape)
print(shares)

# ── 08b. Задача: нормализация по строкам ───────────────────────────────────
print("\n── 08b. Задача: нормализация по строкам ──")
x = np.arange(12, dtype=float).reshape(3, 4)
means = x.mean(axis=1, keepdims=True)
stds = x.std(axis=1, keepdims=True)
znorm = ((x - means) / stds).round(2)
print(means.shape, stds.shape)
print(znorm)
