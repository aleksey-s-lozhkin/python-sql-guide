"""Лаборатория к главе 08: индексация и маски.

Запуск:  python3 guide/snippets/08_indexing_lab.py
"""
import numpy as np

print("numpy", np.__version__)
print("=" * 64)

ages = np.array([22, 31, 25, 40, 19])
salaries = np.array([50000, 90000, 70000, 120000, 45000])

# ─── 1. Маска — это массив bool ───────────────────────────────────
print("\n1) МАСКА: МАССИВ BOOL, А НЕ ФИЛЬТР")
mask = ages > 25
print("   ages        :", ages)
print("   ages > 25   :", mask)
print("   mask.dtype  :", mask.dtype)
print("   ages[mask]  :", ages[mask])
print("   сумма по маске:", mask.sum(), "| count_nonzero:", np.count_nonzero(mask))

# ─── 2. Пример из плана недели 2 ──────────────────────────────────
print("\n2) ПРАКТИКА: СОТРУДНИКИ СТАРШЕ 25 С ЗАРПЛАТОЙ ВЫШЕ 60 000")
both = (ages > 25) & (salaries > 60_000)
print("   маска       :", both)
print("   ages[both]  :", ages[both])
print("   salaries    :", salaries[both])
print("   без скобок  : ages > 25 & salaries > 60_000 → ошибка или не то")

print("\n   зарплаты > 60 000:", salaries[salaries > 60_000])
print("   средняя зарплата :", salaries.mean())
print("   максимальная     :", salaries.max(), "| индекс:", salaries.argmax())
print("   +10%             :", (salaries * 1.1).round().astype(int))

# ─── 3. Двумерная индексация ──────────────────────────────────────
print("\n3) ДВУМЕРНЫЙ МАССИВ: СТРОКА, СТОЛБЕЦ, ПОДМАТРИЦА")
m = np.arange(12).reshape(3, 4)
print("   m:\n", m)
print("   m[0]      :", m[0])
print("   m[:, 0]   :", m[:, 0])
print("   m[1:3, 2:]:\n", m[1:3, 2:])
print("   m[-1, -1] :", m[-1, -1])

# ─── 4. Маска на двумерном массиве ────────────────────────────────
print("\n4) МАСКА РАБОТАЕТ И НА ДВУМЕРНОМ")
print("   m[m % 2 == 0] :", m[m % 2 == 0])
print("   m > 5:\n", m > 5)
print("   m[m > 5]      :", m[m > 5])

# ─── 5. Срез — view, fancy indexing — копия ───────────────────────
print("\n5) СРЕЗ — ОКНО, СПИСОК ИНДЕКСОВ — КОПИЯ")
base = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
view = base[:, 1:3]
fancy = base[[0, 2]]
print("   view.base is base  →", view.base is base)
print("   fancy.base is base →", fancy.base is None)
print("   view.flags.owndata  :", view.flags.owndata)
print("   fancy.flags.owndata :", fancy.flags.owndata)

# ─── 6. np.where: выбрать по условию ──────────────────────────────
print("\n6) NP.WHERE: ВЕКТОРНЫЙ ТЕРНАРНЫЙ ОПЕРАТОР")
print("   where(m > 5, m, 0):\n", np.where(m > 5, m, 0))
print("   нечётные заменить на -1:\n", np.where(m % 2 == 1, -1, m))

# ─── 7. NaN не равен сам себе ─────────────────────────────────────
print("\n7) СРАВНЕНИЕ С NaN ВСЕГДА FALSE")
values = np.array([1.0, np.nan, 3.0])
print("   values > 2  :", values > 2)
print("   np.isnan    :", np.isnan(values))
print("   сумма nan   :", int(np.isnan(values).sum()))

# ─── 8. Fancy indexing и reshape ─────────────────────────────────
print("\n8) СПИСОК ИНДЕКСОВ")
rows = np.array([0, 2])
print("   m[rows]:\n", m[rows])
print("   m[[0, 1], [1, 2]] :", m[[0, 1], [1, 2]], " ← пары (0,1) и (1,2)")
print("=" * 64)
