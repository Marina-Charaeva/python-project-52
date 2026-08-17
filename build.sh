#!/usr/bin/env bash
# build.sh
set -o errexit

# Устанавливаем uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости через pчерез uv
uv sync

#  Создаем директории
mkdir -p staticfiles
mkdir -p media

# Применяем миграции
uv run python manage.py migrate --noinput

# Собираем статику
uv run python manage.py collectstatic --noinput --clear