#!/usr/bin/env bash
# build.sh
set -o errexit

# Python version
python --version

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Создаем директории
mkdir -p staticfiles
mkdir -p media

# Создаем и применяем миграции
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Собираем статику
python manage.py collectstatic --noinput
