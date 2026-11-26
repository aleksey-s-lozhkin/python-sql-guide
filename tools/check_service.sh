#!/bin/bash
# Смоук-тест сервиса практики: аккаунт, прогресс, проверка SQL и защита.
# Использование: bash tools/check_service.sh [http://127.0.0.1:8080]
set -uo pipefail

BASE="${1:-http://127.0.0.1:8080}"
JAR="$(mktemp)"
PASS=0
FAIL=0

check() {
  local name="$1" expected="$2" body="$3"
  if printf '%s' "$body" | grep -q "$expected"; then
    PASS=$((PASS + 1)); printf '  ok   %s\n' "$name"
  else
    FAIL=$((FAIL + 1)); printf '  FAIL %s\n       %s\n' "$name" "$(printf '%s' "$body" | head -c 300)"
  fi
}

json_sql() {
  python3 -c 'import json,sys; print(json.dumps({"sql": sys.stdin.read()}))' <<< "$1"
}

check_sql() {
  local slug="$1" sql="$2" expected="$3" name="$4"
  local payload body
  payload="$(json_sql "$sql")"
  sleep 2.1
  body="$(curl -s -b "$JAR" -X POST "$BASE/api/tasks/$slug/check" \
    -H 'Content-Type: application/json' --data-binary "$payload")"
  check "$name" "$expected" "$body"
}

echo "Сервис: $BASE"
echo "== health =="
body="$(curl -s -m 5 "$BASE/health")"; check "health" '"ok":true' "$body"
body="$(curl -s -m 5 "$BASE/api/tasks")"; check "tasks" '"slug"' "$body"

EMAIL="check$(date +%s)@example.com"
echo "== auth =="
body="$(curl -s -c "$JAR" -X POST "$BASE/api/auth/register" \
  -H 'Content-Type: application/json' \
  --data-binary "{\"email\":\"$EMAIL\",\"password\":\"password123\"}")"
check "register" '"email"' "$body"
body="$(curl -s -b "$JAR" "$BASE/api/me")"; check "me" '"email"' "$body"

echo "== progress =="
body="$(curl -s -b "$JAR" -X PUT "$BASE/api/progress/ch-19-order-of-execution" \
  -H 'Content-Type: application/json' -d '{"status":"done"}')"
check "put" '"ok":true' "$body"
body="$(curl -s -b "$JAR" "$BASE/api/progress")"; check "get" 'ch-19-order-of-execution' "$body"
body="$(curl -s -b "$JAR" -X DELETE "$BASE/api/progress/ch-19-order-of-execution")"
check "delete" '"ok":true' "$body"

echo "== задачи (верные запросы) =="
check_sql top3-users "SELECT u.name, SUM(o.quantity * p.price) AS revenue FROM orders o JOIN users u ON u.id = o.user_id JOIN products p ON p.id = o.product_id GROUP BY u.name ORDER BY revenue DESC LIMIT 3" '"ok":true' "top3-users"
check_sql monthly-revenue "SELECT date_trunc('month', o.created_at)::date AS month, COUNT(*) AS orders, SUM(o.quantity * p.price) AS revenue FROM orders o JOIN products p ON p.id = o.product_id GROUP BY 1 ORDER BY 1" '"ok":true' "monthly-revenue"
check_sql category-share "WITH c AS (SELECT p.category, SUM(o.quantity * p.price) AS revenue FROM orders o JOIN products p ON p.id = o.product_id GROUP BY p.category) SELECT category, revenue, ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS share_pct FROM c ORDER BY revenue DESC" '"ok":true' "category-share"
check_sql guest-orders "SELECT COUNT(*) AS guest_orders, SUM(o.quantity * p.price) AS guest_revenue FROM orders o JOIN products p ON p.id = o.product_id WHERE o.user_id IS NULL" '"ok":true' "guest-orders"

echo "== защита =="
check_sql top3-users "SELECT 1 AS x" '"ok":false' "неверный результат отклонён"
check_sql top3-users "DROP TABLE orders" 'запрещено\|SELECT или WITH' "DROP отклонён"
check_sql top3-users "SELECT 1; SELECT 2" 'один SQL-запрос' "несколько выражений отклонены"
check_sql top3-users "SELECT pg_sleep(10)" 'запрещены' "pg_sleep отклонён"
check_sql top3-users "SELECT email FROM app.users" 'permission denied' "app-схема недоступна"

rm -f "$JAR"
echo
echo "Пройдено: $PASS · Провалено: $FAIL"
[ "$FAIL" -eq 0 ]
