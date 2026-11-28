"""Лаборатория к главе 11: view и copy.

Запуск:  python3 guide/snippets/11_views_copies_lab.py
"""
import numpy as np

print("numpy", np.__version__)
print("=" * 64)

# ─── 1. Срез — окно: правка меняет исходник ───────────────────────
print("\n1) СРЕЗ — VIEW: ПРАВКА ВИДНА В ИСХОДНИКЕ")
base = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
print("   base:\n", base)

view = base[1:, 2:]
print("   view.base is base   :", view.base is base)
print("   view.flags.owndata  :", view.flags.owndata)
view[:] = -1
print("   base после view[:] = -1:\n", base)

# ─── 2. Копия независима ─────────────────────────────────────────
print("\n2) КОПИЯ НЕЗАВИСИМА")
safe = base[[0, 1]].copy()
safe[:] = 0
print("   base не изменился:\n", base)
print("   np.shares_memory(base, safe):", np.shares_memory(base, safe))

# ─── 3. Продвинутая индексация — всегда копия ────────────────────
print("\n3) FANCY INDEXING — КОПИЯ")
fancy = base[[0, 2]]
print("   fancy.base:", fancy.base)
print("   fancy.flags.owndata:", fancy.flags.owndata)
fancy[:] = 99
print("   base не изменился:", base[0].tolist(), base[2].tolist())

# ─── 4. reshape и transpose: обычно view ─────────────────────────
print("\n4) RESHAPE И TRANSPOSE: ОБЫЧНО VIEW")
fresh = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
reshaped = fresh.reshape(1, 9)
transposed = fresh.T
print("   reshape.base is fresh :", reshaped.base is fresh)
print("   transpose.base is fresh:", transposed.base is fresh)
print("   shares_memory(reshape):", np.shares_memory(reshaped, fresh))
print("   shares_memory(transpose):", np.shares_memory(transposed, fresh))
print("   strides transpose:", transposed.strides, "| fresh:", fresh.strides)

# ─── 5. reshape неконтигуозного массива может копировать ─────────
print("\n5) RESHAPE НЕКОНТИГУОЗНОГО МОЖЕТ КОПИРОВАТЬ")
strided = fresh.T                    # транспонирование — view
print("   strided.flags.c_contiguous:", strided.flags.c_contiguous)
flat = strided.reshape(9)            # а вот reshape здесь вынужден скопировать
print("   shares_memory(strided, flat):", np.shares_memory(strided, flat))
print("   flat.flags.owndata:", flat.flags.owndata)

# ─── 6. Как проверить и как скопировать ──────────────────────────
print("\n6) ПРОВЕРКИ И ЯВНОЕ КОПИРОВАНИЕ")
print("   np.shares_memory(base, base[1:]) :", np.shares_memory(base, base[1:]))
print("   np.shares_memory(base, base.copy()):", np.shares_memory(base, base.copy()))
print("   np.may_share_memory(base, base[1:]):", np.may_share_memory(base, base[1:]))

# ─── 7. pandas и Copy-on-Write ───────────────────────────────────
print("\n7) PANDAS 3: COPY-ON-WRITE")
import pandas as pd

print("   pandas", pd.__version__)
df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
series = df["a"]
series.iloc[0] = 99
print("   df после правки series:", df["a"].tolist(), " ← исходник не изменился")
df.loc[0, "a"] = 99
print("   df после df.loc[0, 'a']:", df["a"].tolist(), " ← явное присваивание работает")
print("=" * 64)
