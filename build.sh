#!/usr/bin/env bash
# build.sh
set -o errexit

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости
pip install --upgrade pip
pip install django-bootstrap5 django django-environ dj-database-url gunicorn psycopg2-binary whitenoise
# Собираем статику
python manage.py collectstatic --noinput

# Применяем миграции
python manage.py migrate