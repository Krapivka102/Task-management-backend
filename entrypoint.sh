#!/bin/bash

echo "Starting entrypoint script..."

rm -rf static && ln -s /static static
rm -rf media && ln -s /media media
rm -rf logs && ln -s /logs logs

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

echo "Starting Supervisor..."
python manage.py runserver 0.0.0.0:80