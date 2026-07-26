.PHONY: build render-start

install:
	uv sync

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi:application