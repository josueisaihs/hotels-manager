.PHONY: build up stop test build-test shell


help:
	@echo "build - Build the docker containers"
	@echo "build_clean - Build the docker containers without cache"
	@echo "up - Start the docker containers"
	@echo "stop - Stop the docker containers"
	@echo "test - Run the tests"
	@echo "build-test - Build the test docker containers"
	@echo "shell - Start a shell in the backend container"
	@echo "migrate - Run the migrations"
	@echo "migrations - Create the migrations"
	@echo "collectstatic - Collect the static files"
	@echo "createsuperuser - Create a superuser"
	@echo ""
	@echo "Local use"
	@echo "quick-migrate - Create and run the migrations"
	@echo "coverage-report - Run the tests and generate a coverage report"
	@echo "broker - Start the redis server"
	@echo "celery - Start the celery worker"


build:
	docker-compose build

build_clean:
	docker-compose build --no-cache --pull

up:
	docker-compose up

stop:
	docker-compose stop

test:
	docker-compose -f docker-compose-test.yml up --abort-on-container-exit

build-test:
	docker-compose -f docker-compose-test.yml build

shell:
	docker-compose run --rm backend bash

migrate:
	docker-compose run --rm backend ./manage.py migrate

migrations:
	docker-compose run --rm backend ./manage.py makemigrations

collectstatic:
	docker-compose run --rm backend ./manage.py collectstatic --noinput

coverage-report:
	docker-compose run --rm backend poetry run coverage run --source="app/" manage.py test && docker-compose run --rm backend poetry run coverage report

createsuperuser:
	docker-compose exec backend ./manage.py createsuperuser

# Local development
CMD = ./manage.py

quick-migrate:
	$(CMD) makemigrations && $(CMD) migrate

broker:
	redis-server

celery:
	celery -A app.config worker -l info
