#!/usr/bin/env bash
# build.sh
set -o errexit

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости
uv pip install --upgrade pip
uv pip install django-bootstrap5 django django-environ dj-database-url gunicorn psycopg2-binary whitenoise
# Собираем статику
uv run python manage.py collectstatic --noinput

# Применяем миграции
uv run python manage.py migrate