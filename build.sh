#!/usr/bin/env bash
# build.sh
set -o errexit

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости
uv sync

# Собираем статику
uv run python manage.py collectstatic --noinput

# Применяем миграции
uv run python manage.py migrate