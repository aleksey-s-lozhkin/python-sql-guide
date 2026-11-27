"""Справочник: deque. Все примеры страницы ref-deque.html.

Запуск из корня проекта:
    python3 guide/snippets/ref_deque_lab.py

Вывод не зависит от машины: никакого времени, hash и id.
"""

from collections import deque

# ── 03. Как создать ────────────────────────────────────────────────────────
print("── 03. Как создать ──")
empty = deque()
numbers = deque([10, 20, 30])
chars = deque("abc")
bounded = deque(range(6), maxlen=4)

print(empty)
print(numbers)
print(chars)
print(bounded)
print(bounded.maxlen)

# ── 05. Разбор по группам ─────────────────────────────────────────────────
print("\n── 05.1 Оба конца ──")
q = deque([10, 20, 30])
q.appendleft(0)
q.append(40)
print(q)
print(q.popleft(), q.pop())
print(q)

print("\n── 05.2 extend и extendleft ──")
left = deque([3, 4])
left.extend([5, 6])
right = deque([3, 4])
right.extendleft([1, 2])
print(left)
print(right)

print("\n── 05.3 rotate ──")
q = deque([1, 2, 3, 4, 5])
q.rotate(2)
print(q)
q.rotate(-2)
print(q)

print("\n── 05.4 maxlen ──")
recent = deque(maxlen=3)
for value in [10, 20, 30, 40]:
    recent.append(value)
    print(value, "→", list(recent))

recent.appendleft(5)
print(recent, len(recent), recent.maxlen)

print("\n── 05.5 Доступ ──")
q = deque([10, 20, 30, 20])
print(q[0], q[-1])
print(len(q), 20 in q)
print(list(q))
print(list(reversed(q)))
print(q.count(20), q.index(20))

print("\n── 05.6 Середина ──")
q = deque([10, 20, 30])
q.insert(1, 99)
print(q)
print(q.remove(20))
print(q)
print(q.index(30))

print("\n── 05.7 Копия, разворот, очистка ──")
q = deque([1, 2, 3])
copy = q.copy()
copy.append(4)
print(q, copy)
q.reverse()
print(q)
q.clear()
print(q, len(q))

print("\n── 05.8 Чего нет: срезы и hash ──")
q = deque([1, 2, 3])
try:
    print(q[1:3])
except TypeError as error:
    print("срез:", error)
try:
    print(hash(q))
except TypeError as error:
    print("hash:", error)
print(list(q)[1:3])

# ── 06. Сценарии ──────────────────────────────────────────────────────────
print("\n── 06.1 Очередь задач ──")
tasks = deque(["заказ #101", "заказ #102", "заказ #103"])
tasks.append("заказ #104")
while tasks:
    print("обработан:", tasks.popleft())

print("\n── 06.2 BFS ──")
graph = {
    "Anna": ["Ivan", "Olga"],
    "Ivan": ["Olga"],
    "Olga": ["Petr"],
    "Petr": [],
}


def bfs(start):
    queue = deque([start])
    seen = {start}
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order


print(bfs("Anna"))

print("\n── 06.3 Скользящее окно ──")
prices = [1200, 800, 1500, 900, 1100]
window = deque(maxlen=3)
for price in prices:
    window.append(price)
    print(list(window), "→", round(sum(window) / len(window), 2))


print("\n── 06.4 Rate limiter ──")
class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.hits = deque()

    def allow(self, now):
        while self.hits and now - self.hits[0] >= self.window:
            self.hits.popleft()
        if len(self.hits) >= self.limit:
            return False
        self.hits.append(now)
        return True


limiter = RateLimiter(limit=2, window=10)
for moment in [0, 1, 2, 9, 10, 11]:
    print(moment, limiter.allow(moment))

# ── 07. Ошибки (проверяем, что падает именно так) ──────────────────────────
print("\n── 07. Ошибки ──")
full = deque([1, 2, 3], maxlen=3)
try:
    full.insert(0, 9)
except IndexError as error:
    print("insert в полный deque:", error)

# ── 08. Задачи ────────────────────────────────────────────────────────────
print("\n── 08.1 Палиндром ──")


def is_palindrome(text):
    chars = deque(ch for ch in text.lower() if ch.isalnum())
    while len(chars) > 1:
        if chars.popleft() != chars.pop():
            return False
    return True


print(is_palindrome("А роза упала на лапу Азора"))
print(is_palindrome("python"))

print("\n── 08.2 Скользящее среднее ──")


def moving_average(values, size):
    window = deque(maxlen=size)
    result = []
    for value in values:
        window.append(value)
        if len(window) == size:
            result.append(round(sum(window) / size, 2))
    return result


print(moving_average([1200, 800, 1500, 900, 1100], 3))

# ── 09. Мостик ────────────────────────────────────────────────────────────
print("\n── 09. Буфер последних событий ──")


class LastEvents:
    def __init__(self, size=100):
        self.events = deque(maxlen=size)

    def add(self, event):
        self.events.append(event)


last = LastEvents(3)
for event in ["login", "buy", "logout", "buy"]:
    last.add(event)
print(list(last.events))
