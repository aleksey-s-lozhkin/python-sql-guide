# -*- coding: utf-8 -*-
"""Справочник: str. Все примеры страницы ref-str.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_str_lab.py

Вывод не зависит от машины: никакого времени, hash и id; множества строк не печатаются.
"""


def block(title):
    """Маркер раздела — как в остальных лабораториях книги."""
    print(f"\n── {title} ──")


# ── 03. Как создать ────────────────────────────────────────────────────────
block("03. Как создать")
name = "Anna"                          # литерал в кавычках
empty = ""                             # пустая строка
multi = """первая
вторая"""                              # многострочный литерал
from_parts = "".join(["Ivan", " ", "Petr"])
from_bytes = b"Olga".decode("utf-8")
greeting = f"Привет, {name}!"
print(repr(empty))
print(multi)
print(from_parts)
print(repr(from_bytes))
print(greeting)

print(str(42), type(str(42)).__name__)
print(str(3.5), str(True))
print(len(""), len("бусы"))


# ── 05.1 Неизменяемость, индексы и срезы ───────────────────────────────────
block("05.1 Неизменяемость, индексы и срезы")
s = "бусы"
try:
    s[0] = "Б"
except TypeError as e:
    print(type(e).__name__, e)

new = s.replace("б", "Б")
print(s)
print(new)

word = "бусы"
print(word[0], word[-1], len(word))
print(word[1:3], word[::-1])
print(word[::2])


# ── 05.2 Регистр и обрезка краёв ───────────────────────────────────────────
block("05.2 Регистр и обрезка краёв")
raw = "annA ivanova"
print(raw.upper())
print(raw.lower())
print(raw.capitalize())
print(raw.title())
print("hELLo wORLD".swapcase())
print("STRASSE".lower() == "straße".lower())
print("STRASSE".casefold() == "straße".casefold())

padded = "  anna@mail.ru  "
print(repr(padded.strip()))
print(repr("xxannaxx".strip("x")))
print(repr("xxannaxx".lstrip("x")))
print(repr("xxannaxx".rstrip("x")))
print(repr("https://site.ru".removeprefix("https://")))
print(repr("anna@mail.ru ".removesuffix(" ")))
print(repr("annaxx".removeprefix("xx")))


# ── 05.3 Поиск ─────────────────────────────────────────────────────────────
block("05.3 Поиск")
text = "anna@mail.ru; ivan@mail.ru"
print(text.find("@"))
print(text.rfind("@"))
print(text.find("gmail"))
print(text.count("@"), text.count("mail"))
try:
    text.index("gmail")
except ValueError as e:
    print(type(e).__name__, e)
print(text.startswith("anna"), text.endswith(".ru"))
print(text.startswith(("src/", "anna@")))
print("mail" in text)


# ── 05.4 Разбиение и сборка ────────────────────────────────────────────────
block("05.4 Разбиение и сборка")
line = "Anna;1200;2024-02-01"
print(line.split(";"))
print(line.split(";", 1))
print(line.rsplit(";", 1))
print("a,b,,c".split(","))
print("  Anna   Ivanova  ".split())
text = "первая\nвторая\r\nтретья"
print(text.splitlines())
print("anna@mail.ru".partition("@"))
print("anna@mail.ru".rpartition("@"))
print("no-at-sign".partition("@"))

try:
    "abc".split("")
except ValueError as e:
    print(type(e).__name__, e)

parts = ["Anna", "Olga", "Ivan"]
print(", ".join(parts))
print("-".join("бусы"))
print(", ".join(str(n) for n in [1, 2, 3]))
try:
    ", ".join([1, 2])
except TypeError as e:
    print(type(e).__name__, e)


# ── 05.5 Форматирование и преобразования ──────────────────────────────────
block("05.5 Форматирование и преобразования")
name, amount = "Anna", 1200
print(f"{name}: {amount:,} ₽")
print("{}: {:,} ₽".format(name, amount))
print("%s: %d ₽" % (name, amount))
print("{name}: {amount:,}".format_map({"name": "Olga", "amount": 900}))
print("42".zfill(5))
print("[" + "Анна".ljust(8, ".") + "]")
print("[" + "Анна".rjust(8, ".") + "]")
print("[" + "Анна".center(8, ".") + "]")
print(repr("a\tb\tc".expandtabs(4)))

text = "anna@mail.ru"
print(text.replace("@", " at "))
print(text.replace("m", "M", 1))
print(text.replace(".ru", ""))
print("анна".translate(str.maketrans("ан", "an")))
print("+7 (999) 123-45-67".translate(str.maketrans("", "", " ()-")))


# ── 05.6 Кодировки ────────────────────────────────────────────────────────
block("05.6 Кодировки")
raw = "Анна"
encoded = raw.encode("utf-8")
print(encoded)
print(type(encoded).__name__, len(encoded), len(raw))
print(encoded.decode("utf-8"))
print(b"Anna".decode("ascii"))
try:
    "Анна".encode("ascii")
except UnicodeEncodeError as e:
    print(type(e).__name__)
print(ord("A"), ord("А"), chr(65), chr(1040))
print(str(raw), repr(raw))
try:
    print("сумма: " + 1200)
except TypeError as e:
    print(type(e).__name__, e)


# ── 05.7 Проверки is* ────────────────────────────────────────────────────
block("05.7 Проверки is*")
print("Anna".isalpha(), "Anna 2".isalpha(), "".isalpha())
print("anna".islower(), "ANNA".isupper(), "Anna Ivanova".istitle())
print("py123".isalnum(), "py 123".isalnum())
print("  \t".isspace(), " a ".isspace())
print("hello_world".isidentifier(), "2x".isidentifier())
print("café".isascii(), "cafe".isascii())
print("a b".isprintable(), "\n".isprintable())
print("42".isdigit(), "42".isdecimal(), "42".isnumeric())
print("½".isdigit(), "½".isdecimal(), "½".isnumeric())
print("²".isdigit(), "Ⅳ".isnumeric(), "Ⅳ".isdigit())
number = "-17"
print(number.isdigit(), int(number))
try:
    int("½")
except ValueError as e:
    print(type(e).__name__, e)


# ── 06.1 Нормализация email ────────────────────────────────────────────────
block("06.1 Нормализация email")
def normalize_email(raw):
    return raw.strip().lower()

inbox = ["  Anna@Mail.RU ", "ivan@MAIL.RU", "  Anna@mail.ru"]
clean = [normalize_email(e) for e in inbox]
print(clean)
print(len(clean), len(set(clean)))


# ── 06.2 Разбор CSV-строки ────────────────────────────────────────────────
block("06.2 Разбор CSV-строки")
row = "Ivan;800;2024-03-01"
name, amount, day = row.split(";", 2)
print(name, int(amount), day, sep=" | ")
bad = "Olga;1500"
print(bad.count(";") + 1)
try:
    bad.split(";", 2)[2]
except IndexError as e:
    print(type(e).__name__)


# ── 06.3 Сборка отчёта через join ─────────────────────────────────────────
block("06.3 Сборка отчёта через join")
totals = {"Anna": 1700, "Olga": 1800, "Ivan": 800}
rows = [f"{name:8} {amount:>6,}" for name, amount in totals.items()]
report = "\n".join(rows)
print(report)
print(len(report.splitlines()))


# ── 08.1 Решение: дата из ISO ─────────────────────────────────────────────
block("08.1 Решение: дата из ISO")
date = "2024-02-01"
year, month, day = date.split("-")
print(".".join([day, month, year]))


# ── 08.2 Решение: отчёт из пар ─────────────────────────────────────────────
block("08.2 Решение: отчёт из пар")
lines = ["Anna;1200", "Olga;1500", "Anna;500"]
totals = {}
for line in lines:
    name, amount = line.split(";")
    totals[name] = totals.get(name, 0) + int(amount)
report = "\n".join(f"{name:<6}{amount:>8,}" for name, amount in totals.items())
print(report)
