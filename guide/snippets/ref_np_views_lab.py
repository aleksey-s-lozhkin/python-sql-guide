"""Справочник NumPy: view и copy — все примеры страницы ref-np-views.html.

Требуется numpy 2.3.5 (как в книге).
Запуск из корня проекта:
    python guide/snippets/ref_np_views_lab.py
"""
import numpy as np

np.set_printoptions(linewidth=80)
print("numpy", np.__version__)
print("=" * 56)

# ── 03. View: срез и правка ─────────────────────────────────────────────────
print("\n── 03. View: срез и правка ──")
arr = np.arange(6)
view = arr[1:3]
print(view)
print(view.base is arr, view.flags.owndata)
view[:] = -1
print(arr)

# ── 03. Copy: независимость ─────────────────────────────────────────────────
print("\n── 03. Copy: независимость ──")
arr = np.arange(6)
copy = arr[1:3].copy()
copy[:] = -1
print(arr)
print(np.shares_memory(arr, copy), copy.base is None)

# ── 05. Срез, reshape, ravel, T и flatten ───────────────────────────────────
print("\n── 05. Срез, reshape, ravel, T и flatten ──")
grid = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
print(grid[1].base is grid, grid[:, 2].base is grid)
print(grid.reshape(2, 6).base is grid, grid.T.base is grid)
print(grid.reshape(2, 6).ravel().base is grid)
flat = grid.T.flatten()
print(flat.base is None, np.shares_memory(grid.T, flat))

# ── 05. Fancy и маска ───────────────────────────────────────────────────────
print("\n── 05. Fancy и маска ──")
arr = np.arange(6)
fancy = arr[[0, 2]]
masked = arr[arr % 2 == 0]
print(fancy, fancy.base is None, fancy.flags.owndata)
print(masked, masked.base is None)
print(np.shares_memory(arr, fancy), np.shares_memory(arr, masked))

# ── 05. astype и np.array(copy=...) ─────────────────────────────────────────
print("\n── 05. astype и np.array(copy=...) ──")
arr = np.arange(3)
floats = arr.astype("float64")
print(floats, floats.base is None, np.shares_memory(arr, floats))
same = np.array(arr, copy=False)
print(same is arr, np.shares_memory(arr, same))
try:
    np.array(arr, copy=False, dtype="float64")
except ValueError as e:
    print(type(e).__name__, str(e).splitlines()[0])
print(np.array(arr, copy=None, dtype="float64"))

# ── 05. base, shares_memory и strides ───────────────────────────────────────
print("\n── 05. base, shares_memory и strides ──")
grid = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
col = grid[:, 2]
print(grid.base is None, grid.flags.owndata)
print(col.base is grid, col.strides, col.flags.c_contiguous)
print(np.shares_memory(grid, col), np.may_share_memory(grid, col))
print(grid.T.strides, grid.strides)

# ── 05. writeable и read-only ───────────────────────────────────────────────
print("\n── 05. writeable и read-only ──")
arr = np.arange(4)
print(arr.flags.writeable)
ro = arr.copy()
ro.flags.writeable = False
print(ro[1:3].flags.writeable)
try:
    ro[0] = 9
except ValueError as e:
    print(type(e).__name__, e)
print(ro.copy().flags.writeable)

# ── 05. reshape после несмежного среза ──────────────────────────────────────
print("\n── 05. reshape после несмежного среза ──")
grid = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
t = grid.T
flat = t.reshape(12)
print(t.flags.c_contiguous, flat.flags.owndata)
print(flat.base is None, np.shares_memory(t, flat))
print(flat.base)

# ── 06. Безопасная функция ──────────────────────────────────────────────────
print("\n── 06. Безопасная функция ──")
def clean(data):
    out = data.copy()
    out[out < 0] = 0
    return out

data = np.array([-2, 5, -1, 7])
print(clean(data))
print(data)

# ── 06. Память: view против копии ───────────────────────────────────────────
print("\n── 06. Память: view против копии ──")
big = np.arange(1_000_000)
part = big[:1000]
part_copy = big[:1000].copy()
print(big.nbytes, part.nbytes, part_copy.nbytes)
print(np.shares_memory(big, part), np.shares_memory(big, part_copy))

# ── 06. Окно в матрице ──────────────────────────────────────────────────────
print("\n── 06. Окно в матрице ──")
grid = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
row = grid[1]
col = grid[:, 2]
print(row, row.base is grid)
print(col, col.base is grid)
row[:] = 0
col[:] = 9
print(grid)

# ── 08. Задача 01: отрицательные ────────────────────────────────────────────
print("\n── 08. Задача 01: отрицательные ──")
def zero_negatives(data):
    out = data.copy()
    out[out < 0] = 0
    return out

values = np.array([-2, 5, -1])
print(zero_negatives(values))
print(values)

# ── 08. Задача 02: окно или копия ───────────────────────────────────────────
print("\n── 08. Задача 02: окно или копия ──")
a = np.arange(6)
print(np.shares_memory(a, a[2:5]), np.shares_memory(a, a[[1, 3]]))
print(np.shares_memory(a, a.T), np.shares_memory(a, a[a > 0]))
