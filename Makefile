.PHONY: build up down logs shell test lint migrate

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec api python src/manage.py shell

test:
	poetry run pytest

lint:
	poetry run ruff .

migrate:
	docker-compose exec api python src/manage.py migrate

createapp:
	docker-compose exec api python src/manage.py startapp $(app)

setup:
	cp config.yaml.example config.yaml
	poetry install
	pre-commit install
