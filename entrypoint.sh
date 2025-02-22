#!/bin/bash

echo "Starting entrypoint script..."

# Ждем, пока PostgreSQL станет доступен (если используется)
if [ "$ENGINE" = "django.db.backends.postgresql" ]; then
    echo "Waiting for PostgreSQL to become available..."
    until python manage.py check --database default > /dev/null 2>&1; do
        >&2 echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is up - continuing"
fi

# Применяем миграции
echo "Applying database migrations..."
python manage.py migrate

mkdir -p /static /logs

# Создаём символические ссылки (если их нет)
[ ! -L static ] && rm -rf static && ln -s /static static
[ ! -L logs ] && rm -rf logs && ln -s /logs logs

echo "Starting Supervisor..."
python manage.py runserver 0.0.0.0:80