#!/bin/bash
# Создаёт учебную базу learning_shop и загружает схему с данными.
set -euo pipefail
cd "$(dirname "$0")/.."

PGHOST="${PGHOST:-127.0.0.1}"
DB="${DB:-learning_shop}"

if ! psql -h "$PGHOST" -lqt | cut -d '|' -f 1 | grep -qw "$DB"; then
  createdb -h "$PGHOST" "$DB"
  echo "Создана база $DB"
fi

psql -h "$PGHOST" -d "$DB" -q -f guide/snippets/learning_shop.sql
echo "Схема и данные загружены в $DB"

psql -h "$PGHOST" -d "$DB" -c "SELECT 'users' AS table, COUNT(*) FROM users
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'orders', COUNT(*) FROM orders;"
