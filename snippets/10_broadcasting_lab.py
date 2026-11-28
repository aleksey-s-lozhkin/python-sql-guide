"""Лаборатория к главе 10: broadcasting.

Запуск:  python3 guide/snippets/10_broadcasting_lab.py
"""
import numpy as np

print("numpy", np.__version__)
print("=" * 64)

a = np.arange(12).reshape(3, 4)
print("a:\n", a)
print("a.shape:", a.shape)

# ─── 1. Строка (4,) прибавляется к каждой строке ──────────────────
print("\n1) (3, 4) + (4,) → (3, 4): ВЕКТОР ПРИКЛАДЫВАЕТСЯ К КАЖДОЙ СТРОКЕ")
row = np.array([10, 20, 30, 40])
print("   row:", row, "| shape", row.shape)
print("   a + row:\n", a + row)

# ─── 2. Столбец (3, 1) прибавляется к каждой строке ───────────────
print("\n2) (3, 4) + (3, 1) → (3, 4): СТОЛБЕЦ ПРИКЛАДЫВАЕТСЯ К КАЖДОЙ СТРОКЕ")
col = np.array([[100], [200], [300]])
print("   col.shape:", col.shape)
print("   a + col:\n", a + col)

# ─── 3. (3,1) и (1,4) дают (3,4) ─────────────────────────────────
print("\n3) (3, 1) + (1, 4) → (3, 4)")
ones_col = np.ones((3, 1))
ones_row = np.ones((1, 4))
print("   shapes:", ones_col.shape, "+", ones_row.shape, "→", (ones_col + ones_row).shape)
print("   результат:\n", ones_col + ones_row)

# ─── 4. Несовместимые формы ──────────────────────────────────────
print("\n4) НЕСОВМЕСТИМЫЕ ФОРМЫ")
try:
    a + np.array([1, 2, 3])
except ValueError as e:
    print("   ValueError:", str(e).split("\n")[0])

# ─── 5. Центрирование по столбцам через keepdims ─────────────────
print("\n5) ЦЕНТРИРОВАНИЕ: KEEPDIMS РЕШАЕТ ПРОБЛЕМУ ФОРМЫ")
means = a.mean(axis=0)
print("   means.shape:", means.shape)
print("   a - means:\n", a - means)
means_keep = a.mean(axis=0, keepdims=True)
print("   means_keep.shape:", means_keep.shape)
print("   a - means_keep:\n", a - means_keep)
print("   средние после центрирования:", (a - means_keep).mean(axis=0))

# ─── 6. broadcast_to: view без копирования ───────────────────────
print("\n6) BROADCAST_TO: ПРЕДСТАВЛЕНИЕ БЕЗ КОПИРОВАНИЯ")
stamp = np.array([1, 2, 3])
big = np.broadcast_to(stamp, (2, 3))
print("   big.shape:", big.shape, "| strides:", big.strides)
print("   writeable:", big.flags.writeable)
print("   big:\n", big)

# ─── 7. newaxis и reshape ────────────────────────────────────────
print("\n7) НОВАЯ ОСЬ: NEWAXIS И RESHAPE")
v = np.array([1, 2, 3])
print("   v[:, np.newaxis].shape:", v[:, np.newaxis].shape)
print("   v.reshape(-1, 1).shape :", v.reshape(-1, 1).shape)
print("   v[:, None] * v[None, :]:\n", v[:, None] * v[None, :], " ← таблица умножения")
print("=" * 64)
