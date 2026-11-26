# Сервис практики: развёртывание

FastAPI + PostgreSQL в Docker Compose. Книга (`../guide/`) остаётся статической на GitHub Pages;
сервис — отдельный слой с аккаунтами, прогрессом и проверкой SQL-задач.

## Быстрый старт (локально)

```bash
cd deploy
cp .env.example .env          # при желании поменяйте пароли
docker compose up -d --build
docker compose ps
curl -s localhost:8080/health
```

Откройте <http://localhost:8080/> — регистрация, задачи, проверка SQL.

Данные базы лежат в томе `pgdata`. Пересоздать начисто:

```bash
docker compose down -v
docker compose up -d --build
```

## Прод: домен и TLS

Ниже — вариант «свой сервер + Caddy»: Caddy сам получает сертификат Let's Encrypt.

1. **DNS.** У регистратора создайте `A`-запись: `app.example.com → <IP сервера>`.
   Если сервер за NAT — нужен проброс 80/443 либо туннель.
2. **Порты.** Откройте 80 и 443 на сервере (`ufw allow 80,443/tcp`), если включён фаервол.
3. **.env** (рядом с `docker-compose.yml`):

```env
DOMAIN=app.example.com
POSTGRES_PASSWORD=<длинный случайный пароль>
LEARNER_PASSWORD=<другой длинный случайный пароль>
COOKIE_SECURE=1
ALLOWED_ORIGIN=https://app.example.com
API_BIND=127.0.0.1
API_PORT=8080
```

4. **Запуск с Caddy:**

```bash
docker compose --profile prod up -d --build
docker compose logs -f caddy   # первый выпуск сертификата
```

Проверьте: `curl -I https://app.example.com/health`.

Важно: `API_BIND=127.0.0.1` закрывает приложение от прямого доступа извне — снаружи только Caddy.

## Бэкапы

```bash
# дамп в файл (cron: каждый день в 3:00)
docker compose exec -T db pg_dump -U guide -d learning_shop -Fc > /backup/shop_$(date +%F).dump
```

Храните 7–14 дампов, раз в месяц проверяйте восстановление:

```bash
docker compose exec -T db pg_restore -U guide -d learning_shop_restore < /backup/shop_2026-01-01.dump
```

## Обновление

```bash
git pull
docker compose build api
docker compose up -d
```

Паузы в обслуживании нет: `api` перезапускается быстро, Postgres не трогается.

## Безопасность

- SQL ученика выполняется под ролью `learner_ro` — только `SELECT` на `public`, без доступа к `app`.
- Разрешён один запрос, начинающийся с `SELECT`/`WITH`; DML/DDL, `COPY`, `pg_*`, транзакции и
  несколько выражений запрещены.
- `statement_timeout` 3 с, лимит строк 100, read-only транзакция.
- Пароли — PBKDF2-SHA256 (300 000 итераций), сессии — HttpOnly-cookie, токен хранится хэшем.
- В проде обязательно: `COOKIE_SECURE=1`, `ALLOWED_ORIGIN=https://…`, сильные пароли БД,
  не публиковать порт 5432.
- Ограничение: это учебный сервис, не продовая база. Не кладите туда реальные данные.

## Переменные окружения

| Переменная | По умолчанию | Зачем |
|---|---|---|
| `DOMAIN` | `localhost` | домен для Caddy |
| `POSTGRES_PASSWORD` | `guide` | пароль пользователя БД `guide` |
| `LEARNER_PASSWORD` | `learner_ro_dev` | пароль роли `learner_ro` |
| `COOKIE_SECURE` | `0` | `1` — cookie только по https |
| `ALLOWED_ORIGIN` | пусто | разрешённый Origin для POST/PUT/DELETE |
| `API_BIND` | `0.0.0.0` | адрес, на который публикуется API |
| `API_PORT` | `8080` | внешний порт API |
| `SESSION_DAYS` | `30` | срок жизни сессии |

## Диагностика

```bash
docker compose ps
docker compose logs --tail=100 api
docker compose exec db psql -U guide -d learning_shop -c "select count(*) from orders;"
```

Если API падает на старте: проверьте, что база поднялась (`depends_on: condition: service_healthy`)
и что `learning_shop` создана init-скриптом (он выполняется только при пустом томе).
