.PHONY: help up down build test lint scan tf-init tf-validate helm-lint seed load-test clean

PROJECT_NAME := podiumhq
DOCKER_COMPOSE := docker compose

help:
	@echo "PodiumHQ — DevSecOps Automation Commands"
	@echo "----------------------------------------"
	@echo "  make up          : Start full local stack via Docker Compose"
	@echo "  make down        : Stop local stack and remove containers"
	@echo "  make build       : Build backend and frontend images"
	@echo "  make test        : Run pytest suite with coverage gate"
	@echo "  make lint        : Run ruff check and frontend lint"
	@echo "  make scan        : Run security scans (trivy / audit)"
	@echo "  make tf-init     : Initialize Terraform (no backend)"
	@echo "  make tf-validate : Validate Terraform IaC configuration"
	@echo "  make helm-lint   : Strict lint of the Helm chart"
	@echo "  make seed        : Seed initial sample data into database"
	@echo "  make load-test   : Execute HPA load test generator"
	@echo "  make clean       : Clean temporary files and caches"

up:
	$(DOCKER_COMPOSE) up --build -d

down:
	$(DOCKER_COMPOSE) down -v

build:
	$(DOCKER_COMPOSE) build

test:
	cd backend && python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=80

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

scan:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image $(PROJECT_NAME)-backend:latest || true

tf-init:
	cd terraform && terraform init -backend=false

tf-validate:
	cd terraform && terraform fmt -check && terraform validate

helm-lint:
	helm lint helm/podiumhq --strict

seed:
	python -m backend.app.services.seed_data

load-test:
	python scripts/load-test.py --rps 40 --duration 120

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache backend/.pytest_cache frontend/dist
