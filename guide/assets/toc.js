/* Оглавление книги. Один источник правды для навигации и прогресса. */
window.BOOK = {
  title: "Ассоциативный гайд",
  subtitle: "Python → pandas → SQL",
  chapters: [
    // ── I. Фундамент Python ────────────────────────────────────
    { n: "01", slug: "ch-01-python-collections", title: "Карта коллекций: что выбрать и почему", desc: "Неделя 1 · вводная", part: 1, ready: true },
    { n: "02", slug: "ch-02-dict", title: "dict: шкаф с номерками", desc: "Неделя 1", part: 1, ready: true },
    { n: "03", slug: "ch-03-list-tuple", title: "list и tuple: поезд и опечатанный контейнер", desc: "Неделя 1", part: 1, ready: true },
    { n: "04", slug: "ch-04-set", title: "set: пропускной пункт без дублей", desc: "Неделя 1", part: 1, ready: true },
    { n: "05", slug: "ch-05-comprehensions", title: "Comprehensions и генераторы: конвейер против склада", desc: "Неделя 1", part: 1, ready: true },
    { n: "06", slug: "ch-06-collections", title: "Counter, defaultdict, deque: три специнструмента", desc: "Неделя 1", part: 1, ready: true },
    // ── II. NumPy ──────────────────────────────────────────────
    { n: "07", slug: "ch-07-ndarray", title: "ndarray: сетка вместо списка", desc: "Неделя 2", part: 2, ready: true },
    { n: "08", slug: "ch-08-indexing", title: "Индексация и маски: трафарет поверх сетки", desc: "Неделя 2", part: 2, ready: true },
    { n: "09", slug: "ch-09-axis", ready: true, title: "axis: вдоль какой стены считать", desc: "Неделя 2", part: 2 },
    { n: "10", slug: "ch-10-broadcasting", ready: true, title: "Broadcasting: штамп и тесто", desc: "Неделя 2", part: 2 },
    { n: "11", slug: "ch-11-views-copies", ready: true, title: "View и copy: стекло и ксерокс", desc: "Неделя 2", part: 2 },
    // ── III. pandas ────────────────────────────────────────────
    { n: "12", slug: "ch-12-series-dataframe", title: "Series и DataFrame: таблица с оглавлением", desc: "Неделя 3", part: 3, ready: true },
    { n: "13", slug: "ch-13-loc-iloc", title: "loc и iloc: имя против номера", desc: "Неделя 3", part: 3, ready: true },
    { n: "14", slug: "ch-14-filtering", title: "Фильтрация: булева маска как сито", desc: "Неделя 3", part: 3, ready: true },
    { n: "15", slug: "ch-15-groupby", title: "groupby: разложить — посчитать — собрать", desc: "Неделя 4", part: 3, ready: true },
    { n: "16", slug: "ch-16-merge", title: "merge: кардинальность важнее синтаксиса", desc: "Неделя 5", part: 3, ready: true },
    { n: "17", slug: "ch-17-missing", title: "Пропуски: NaN, None и pd.NA", desc: "Неделя 4", part: 3, ready: true },
    { n: "18", slug: "ch-18-dates-reshape", title: "Даты, строки и форма таблицы", desc: "Неделя 5", part: 3, ready: true },
    // ── IV. SQL ────────────────────────────────────────────────
    { n: "19", slug: "ch-19-order-of-execution", title: "Порядок выполнения: как база читает запрос", desc: "Неделя 6", part: 4, ready: true },
    { n: "20", slug: "ch-20-select-where-null", title: "SELECT, WHERE и логика трёх значений", desc: "Неделя 6", part: 4, ready: true },
    { n: "21", slug: "ch-21-group-by-having", title: "GROUP BY и HAVING: тот же словарь-аккумулятор", desc: "Неделя 6", part: 4, ready: true },
    { n: "22", slug: "ch-22-subqueries-cte", title: "Подзапросы и CTE: как разложить вопрос", desc: "Неделя 7", part: 4, ready: true },
    { n: "23", slug: "ch-23-window-functions", title: "Оконные функции: агрегат без схлопывания", desc: "Неделя 7", part: 4, ready: true },
    { n: "24", slug: "ch-24-indexes-explain", title: "Индексы и EXPLAIN: где тормозит запрос", desc: "Неделя 7", part: 4, ready: true },
    // ── V. Интеграция ──────────────────────────────────────────
    { n: "25", slug: "ch-25-sql-vs-pandas", title: "SQL или pandas: что где делать", desc: "Неделя 8", part: 5, ready: true },
    { n: "26", slug: "ch-26-project", title: "Проект: отчёт из нескольких таблиц", desc: "Неделя 8", part: 5, ready: true }
  ],
  parts: [
    { n: 1, title: "Фундамент Python", range: "Неделя 1" },
    { n: 2, title: "NumPy", range: "Неделя 2" },
    { n: 3, title: "pandas", range: "Недели 3–5" },
    { n: 4, title: "SQL", range: "Недели 6–7" },
    { n: 5, title: "Интеграция", range: "Неделя 8" }
  ]
};
