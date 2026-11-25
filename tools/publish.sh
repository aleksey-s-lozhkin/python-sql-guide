#!/bin/bash
# Публикация книги в ветку gh-pages (то же, что делает GitHub Actions).
# Использование: tools/publish.sh ["сообщение коммита"]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MSG="${1:-deploy: $(date '+%Y-%m-%d %H:%M')}"
TMP="$(mktemp -d)"

cd "$ROOT"
cleanup() { git worktree remove "$TMP" --force >/dev/null 2>&1 || rm -rf "$TMP"; }
trap cleanup EXIT

git worktree add --detach "$TMP" >/dev/null
cd "$TMP"
git checkout --orphan gh-pages >/dev/null 2>&1
git rm -rf . >/dev/null 2>&1 || true
cp -R "$ROOT/guide/." .
touch .nojekyll

git add -A
git -c user.name="asl" -c user.email="alseksey.s.lozhkin@gmail.com" commit -q -m "$MSG"
git push --force origin gh-pages

echo "Опубликовано: https://aleksey-s-lozhkin.github.io/python-sql-guide/"
