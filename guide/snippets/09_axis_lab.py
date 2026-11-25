"""Лаборатория к главе 09: axis.

Запуск:  python3 guide/snippets/09_axis_lab.py
"""
import numpy as np

print("numpy", np.__version__)
print("=" * 64)

m = np.arange(12).reshape(3, 4)
print("m:\n", m)
print("shape:", m.shape, "| ndim:", m.ndim)

# ─── 1. Суммы по осям ─────────────────────────────────────────────
print("\n1) AXIS=0 И AXIS=1: ОДНА ОСЬ ИСЧЕЗАЕТ ИЗ РЕЗУЛЬТАТА")
print("   sum(axis=0) →", m.sum(axis=0), "| shape", m.sum(axis=0).shape)
print("   sum(axis=1) →", m.sum(axis=1), "| shape", m.sum(axis=1).shape)
print("   sum()       →", m.sum(), "| shape", m.sum().shape)

# ─── 2. Средние и максимумы ──────────────────────────────────────
print("\n2) СРЕДНИЕ И МАКСИМУМЫ ПО ОСЯМ")
print("   mean(axis=0) →", m.mean(axis=0))
print("   mean(axis=1) →", m.mean(axis=1))
print("   max(axis=1)  →", m.max(axis=1))
print("   argmax(axis=0) →", m.argmax(axis=0))
print("   argmax(axis=1) →", m.argmax(axis=1))

# ─── 3. keepdims: сохранить ось ───────────────────────────────────
print("\n3) KEEPDIMS: ОСТАВИТЬ ОСЬ ДЛЯ BROADCASTING")
print("   sum(axis=0)               shape:", m.sum(axis=0).shape)
print("   sum(axis=0, keepdims=True) shape:", m.sum(axis=0, keepdims=True).shape)
print("   результат:\n", m.sum(axis=0, keepdims=True))

# ─── 4. Отрицательные оси ────────────────────────────────────────
print("\n4) ОТРИЦАТЕЛЬНЫЕ ОСИ")
print("   sum(axis=-1) == sum(axis=1):", np.array_equal(m.sum(axis=-1), m.sum(axis=1)))
print("   sum(axis=-2) == sum(axis=0):", np.array_equal(m.sum(axis=-2), m.sum(axis=0)))

# ─── 5. Несколько осей и 3D ──────────────────────────────────────
print("\n5) НЕСКОЛЬКО ОСЕЙ И ТРЁХМЕРНЫЙ МАССИВ")
cube = np.arange(24).reshape(2, 3, 4)
print("   cube.shape:", cube.shape)
print("   sum(axis=0).shape:", cube.sum(axis=0).shape)
print("   sum(axis=(0, 2)).shape:", cube.sum(axis=(0, 2)).shape, "| значения:", cube.sum(axis=(0, 2)))

# ─── 6. Ось как «направление», а не «что остаётся» ────────────────
print("\n6) ПОЧЕМУ ЛЕГКО ПЕРЕПУТАТЬ")
print("   axis=0: 3 строки схлопываются → 4 числа (по одному на столбец)")
print("   axis=1: 4 столбца схлопываются → 3 числа (по одному на строку)")
print("   фактический результат axis=0:", m.sum(axis=0))

# ─── 7. Ошибка оси ────────────────────────────────────────────────
print("\n7) ОСЬ ВНЕ ДИАПАЗОНА")
try:
    m.sum(axis=2)
except np.exceptions.AxisError as e:
    print("   AxisError:", str(e).split("\n")[0])

# ─── 8. pandas: те же оси ────────────────────────────────────────
print("\n8) PANDAS: ТА ЖЕ ЛОГИКА")
import pandas as pd

df = pd.DataFrame(m, columns=["q1", "q2", "q3", "q4"], index=["anna", "ivan", "olga"])
print(df)
print("   df.sum(axis=0):\n", df.sum(axis=0))
print("   df.sum(axis=1):\n", df.sum(axis=1))
print("=" * 64)
