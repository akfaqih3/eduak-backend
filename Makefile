.PHONY: help install migrate run test clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make migrate       - Run database migrations"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean Python cache files"
	@echo "  make docker-build - Build Docker containers"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f
