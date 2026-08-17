.PHONY: install migrate collectstatic build render-start

install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	uv run python manage.py migrate
	uv run gunicorn -w 5 -b 0.0.0.0:$${PORT:-10000} task_manager.wsgi:application