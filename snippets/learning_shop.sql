-- Учебная база для части IV: users, products, orders.
-- Запуск:  createdb learning_shop && psql -d learning_shop -f guide/snippets/learning_shop.sql
-- Или:     bash tools/setup_db.sh

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    city  TEXT,
    email TEXT
);

CREATE TABLE products (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    category TEXT NOT NULL,
    price    NUMERIC(10, 2) NOT NULL CHECK (price > 0)
);

CREATE TABLE orders (
    id         INTEGER PRIMARY KEY,
    user_id    INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP NOT NULL
);

INSERT INTO users (id, name, city, email) VALUES
    (1, 'Anna',  'Москва',           'anna@mail.ru'),
    (2, 'Ivan',  'Казань',           'ivan@mail.ru'),
    (3, 'Olga',  'Москва',           'olga@mail.ru'),
    (4, 'Petr',  NULL,               'petr@mail.ru'),
    (5, 'Maria', 'Санкт-Петербург',  NULL);

INSERT INTO products (id, name, category, price) VALUES
    (1, 'Ноутбук', 'electronics', 75000.00),
    (2, 'Мышь',    'electronics',  1500.00),
    (3, 'Книга',   'books',         900.00),
    (4, 'Кофе',    'food',          450.00),
    (5, 'Монитор', 'electronics', 22000.00),
    (6, 'Чай',     'food',          300.00);

INSERT INTO orders (id, user_id, product_id, quantity, created_at) VALUES
    (1, 1,    1, 1, '2024-01-05 10:00:00'),
    (2, 2,    3, 2, '2024-01-06 12:30:00'),
    (3, 1,    4, 3, '2024-01-15 09:15:00'),
    (4, 3,    2, 1, '2024-02-01 14:00:00'),
    (5, 2,    5, 1, '2024-02-10 16:45:00'),
    (6, 5,    4, 5, '2024-02-20 11:20:00'),
    (7, 1,    6, 2, '2024-03-03 08:05:00'),
    (8, NULL, 3, 1, '2024-03-07 19:30:00'),
    (9, 3,    1, 1, '2024-03-15 13:10:00'),
    (10, 4,   5, 1, '2024-03-20 15:55:00');
