
.PHONY: install migrate collectstatic build start render-start

install:
	poetry install

migrate:
	poetry run python manage.py migrate

collectstatic:
	poetry run python manage.py collectstatic --noinput

build:
	./build.sh

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

render-start:
	poetry run python manage.py migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application