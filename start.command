#!/bin/bash
# Двойной щелчок: локальный сервер + открыть книгу в браузере.
# Нужен для проверки PWA (офлайн-кэш работает только на http/https, не на file://).
cd "$(dirname "$0")" || exit 1
PORT="${PORT:-8899}"

if lsof -i ":$PORT" >/dev/null 2>&1; then
  echo "Порт $PORT уже занят — открываю существующий сервер."
  open "http://127.0.0.1:$PORT/guide/index.html"
  exit 0
fi

python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null' EXIT INT TERM

sleep 0.8
open "http://127.0.0.1:$PORT/guide/index.html"
echo "Сервер: http://127.0.0.1:$PORT/guide/index.html"
echo "Закройте это окно, чтобы остановить сервер."
wait $SERVER_PID
