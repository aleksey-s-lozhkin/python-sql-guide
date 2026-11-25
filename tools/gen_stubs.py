# -*- coding: utf-8 -*-
import os, html

CH = [
 ("01","ch-01-python-collections","Списки и словари: как думать коллекциями",1,"Неделя 1 · дни 1–2",
  ["список как «поезд»: индексы, срезы, распаковка","словарь как «шкаф с номерками»: вход и выход","первая практика: 5 задач на список словарей без pandas"]),
 ("03","ch-03-list-tuple","list и tuple: поезд и опечатанный контейнер",1,"Неделя 1 · день 1",
  ["изменяемость как причина, по которой tuple можно в ключи","срезы: копия или представление","распаковка, enumerate и zip без лишних индексов"]),
 ("04","ch-04-set","set: пропускной пункт без дублей",1,"Неделя 1 · день 3",
  ["уникальность за O(1) и почему это дешевле list","пересечение, объединение, разность на примерах","когда set проигрывает dict: порядок и хранение пар"]),
 ("05","ch-05-comprehensions","Comprehensions и генераторы: конвейер против склада",1,"Неделя 1 · день 4",
  ["list/dict/set comprehension: три формы одной идеи","генератор: ленивый конвейер и цена повторного обхода","когда comprehension вредит читаемости"]),
 ("06","ch-06-collections","Counter, defaultdict, deque: три специнструмента",1,"Неделя 1 · день 5",
  ["Counter: частоты и most_common","defaultdict: фабрика значений и неявные вставки","deque: очередь с O(1) на обоих концах"]),
 ("07","ch-07-ndarray","ndarray: сетка вместо списка",2,"Неделя 2 · день 1",
  ["shape, ndim, dtype, size: паспорт массива","непрерывная память и почему это быстрее списка","создание массивов: array, zeros, arange, linspace"]),
 ("08","ch-08-indexing","Индексация и маски: трафарет поверх сетки",2,"Неделя 2 · день 2",
  ["срезы по осям и шаг","boolean indexing: трафарет по условию","fancy indexing и его отличие от срезов"]),
 ("09","ch-09-axis","axis: вдоль какой стены считать",2,"Неделя 2 · день 3",
  ["axis=0 и axis=1 без заучивания","keepdims и сохранение формы","агрегаты: sum, mean, max, argmax"]),
 ("10","ch-10-broadcasting","Broadcasting: штамп и тесто",2,"Неделя 2 · день 4",
  ["правила выравнивания форм","почему (3,1) и (1,4) дают (3,4)","типичные ошибки формы и как их читать"]),
 ("11","ch-11-views-copies","View и copy: стекло и ксерокс",2,"Неделя 2 · день 5",
  ["когда срез — это окно, а когда копия","изменение через view и неожиданные эффекты","np.array против np.asarray"]),
 ("12","ch-12-series-dataframe","Series и DataFrame: таблица с оглавлением",3,"Неделя 3 · день 1",
  ["Series = индекс + значения; DataFrame = набор Series","чтение CSV: dtype, usecols, parse_dates","первые проверки: head, info, describe"]),
 ("13","ch-13-loc-iloc","loc и iloc: имя против номера",3,"Неделя 3 · дни 4–5",
  ["метка против позиции: главный источник ошибок","строки и столбцы в одном срезе","df[\"salary\"] против df[[\"salary\"]]"]),
 ("14","ch-14-filtering","Фильтрация: булева маска как сито",3,"Неделя 3 · день 5",
  ["как устроена маска и почему она работает","несколько условий: & | ~ и скобки","query() и когда он читается лучше"]),
 ("15","ch-15-groupby","groupby: разложить — посчитать — собрать",3,"Неделя 4 · день 3",
  ["split-apply-combine на одном рисунке","agg против transform: форма результата","groupby и dict-аккумулятор из главы 02"]),
 ("16","ch-16-merge","merge: кардинальность важнее синтаксиса",3,"Неделя 5 · дни 1–2",
  ["типы JOIN и что происходит со строками","many-to-many: неожиданное размножение","validate и indicator как защита от ошибок"]),
 ("17","ch-17-missing","Пропуски: NaN, None и pd.NA",3,"Неделя 4 · день 4",
  ["три вида отсутствия и зачем они нужны","isna, fillna, dropna: что менять, а что нет","пропуск как сигнал, а не как ноль"]),
 ("18","ch-18-dates-reshape","Даты, строки и форма таблицы",3,"Неделя 5 · дни 3–5",
  ["to_datetime, dt-аксессоры, ресемплирование","str-аксессоры и нормализация текста","pivot, melt, explode: превращения формы"]),
 ("19","ch-19-order-of-execution","Порядок выполнения: как база читает запрос",4,"Неделя 6 · день 1",
  ["FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT","почему алиас из SELECT не виден в WHERE","порядок как инструмент отладки"]),
 ("20","ch-20-select-where-null","SELECT, WHERE и логика трёх значений",4,"Неделя 6 · дни 2–3",
  ["TRUE, FALSE и UNKNOWN: почему NULL = NULL не TRUE","IN, BETWEEN, LIKE и их ловушки","COUNT(*) против COUNT(column)"]),
 ("21","ch-21-group-by-having","GROUP BY и HAVING: тот же словарь-аккумулятор",4,"Неделя 6 · день 4",
  ["WHERE фильтрует строки, HAVING — группы","агрегаты и NULL внутри них","JOIN и GROUP BY: размножение строк"]),
 ("22","ch-22-subqueries-cte","Подзапросы и CTE: как разложить вопрос",4,"Неделя 7 · дни 1–2",
  ["скалярный, коррелированный подзапрос, EXISTS","WITH: читаемость против производительности","как разбить сложный вопрос на шаги"]),
 ("23","ch-23-window-functions","Оконные функции: строка и её группа",4,"Неделя 7 · дни 3–4",
  ["OVER, PARTITION BY и порядок внутри окна","ROW_NUMBER, RANK, DENSE_RANK: три разных ответа","LAG/LEAD и накопительные суммы"]),
 ("24","ch-24-indexes-explain","Индексы и EXPLAIN: верить плану, а не догадкам",4,"Неделя 7 · день 5",
  ["B-tree как оглавление книги","почему индекс не используется и как это увидеть","EXPLAIN против EXPLAIN ANALYZE"]),
 ("25","ch-25-sql-vs-pandas","SQL или pandas: где считать",5,"Неделя 8 · дни 1–3",
  ["фильтровать и агрегировать — в базе","read_sql, параметры, пагинация","сравнение результатов SQL и pandas"]),
 ("26","ch-26-project","Проект: аналитика заказов интернет-магазина",5,"Неделя 8 · дни 4–5",
  ["схема из трёх таблиц и учебная БД PostgreSQL","запросы с JOIN, GROUP BY и оконной функцией","отчёт, проверка качества данных, EXPLAIN"]),
]

PART_TITLE = {1:"Часть I · Фундамент Python",2:"Часть II · NumPy",3:"Часть III · pandas",4:"Часть IV · SQL",5:"Часть V · Интеграция"}
ORDER = ["01","ch-02-dict"]  # 02 is the demo; build neighbor map from full list
FULL = [(n,s,t,p,w,b) for (n,s,t,p,w,b) in CH]
FULL.insert(1, ("02","ch-02-dict","dict: шкаф с номерками",1,"Неделя 1 · день 2", []))

TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{n} · {title} — Ассоциативный гайд</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-slug="{slug}">
<div class="app">
  <aside class="sidebar" id="sidebar"></aside>
  <main>
    <div class="wrap">
      <header class="chapter-head">
        <div class="eyebrow">
          <span class="part">{part}</span><span class="dot"></span><span>{week}</span><span class="dot"></span><span>в работе</span>
        </div>
        <h1>{title}<span class="sub">Глава ещё не написана — сейчас она в очереди по программе</span></h1>
        <p class="lead">Здесь появится тот же формат, что в главе 02: ассоциация-якорь, схема, запускаемый код, разбор типичных ошибок, вопросы с собеседования и задачи с решениями.</p>
        <div class="meta">
          <span class="chip">📐 <b>1 схема</b></span>
          <span class="chip">💻 <b>лаборатория</b></span>
          <span class="chip">🎤 <b>6–8 вопросов</b></span>
          <span class="chip">✍️ <b>3 задачи</b></span>
        </div>
      </header>

      <section>
        <h2><span class="num">01</span>Что войдёт в главу</h2>
        <ol class="chain">
{bullets}
        </ol>
        <div class="note">
          <span class="t">Пока это заглушка</span>
          <p>Заглушка нужна, чтобы оглавление и мостики работали как карта: видно, куда ведёт каждая тема. Начните с готовой главы 02 — она задаёт шаблон для всех остальных.</p>
        </div>
      </section>

      <div class="pager">
        <a class="prev" href="{prev_href}"><span class="dir">← Назад</span><span class="ttl">{prev}</span></a>
        <a class="next" href="{next_href}"><span class="dir">Дальше →</span><span class="ttl">{next}</span></a>
      </div>
    </div>
  </main>
</div>
<script src="assets/toc.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
"""

os.makedirs("guide", exist_ok=True)
for i, (n, slug, title, part, week, bullets) in enumerate(FULL):
    if slug == "ch-02-dict":
        continue
    prev_n, prev_slug, prev_title = ("—", "index.html", "Обложка") if i == 0 else (FULL[i-1][0], FULL[i-1][1] + ".html", FULL[i-1][2])
    if i + 1 < len(FULL):
        next_href, next_title = FULL[i+1][1] + ".html", FULL[i+1][0] + " · " + FULL[i+1][2]
    else:
        next_href, next_title = "index.html", "Обложка и оглавление"
    def split_bullet(b):
        for sep in (": ", " — "):
            if sep in b:
                h, t = b.split(sep, 1)
                return h.strip(), t.strip()
        return b.strip(), ""
    bl = "\n".join(
        (lambda h, t: f"          <li><b>{h}</b>" + (f"<span>{t}</span>" if t else "") + "</li>")(*split_bullet(b))
        for b in bullets
    )
    out = TEMPLATE.format(n=n, slug=slug, title=html.escape(title), part=PART_TITLE[part], week=week,
                          bullets=bl, prev_href=prev_slug, prev=html.escape(prev_title),
                          next_href=next_href, next=html.escape(next_title))
    open(f"guide/{slug}.html", "w", encoding="utf-8").write(out)
    print("stub", slug)
