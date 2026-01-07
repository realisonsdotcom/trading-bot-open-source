SHELL := /bin/bash

.PHONY: setup dev-up dev-down demo-up demo-down native-up native-down lint test e2e e2e-sh migrate-generate migrate-up migrate-down \
	web_dashboard-e2e

ALEMBIC_CONFIG ?= infra/migrations/alembic.ini
ALEMBIC_DATABASE_URL ?= postgresql+psycopg2://trading:trading@localhost:5432/trading
REVISION ?= head
DOWN_REVISION ?= -1
PRE_COMMIT_CONFIG ?= config/pre-commit-config.yaml
REQUIREMENTS_DEV ?= requirements/requirements-dev.txt
COVERAGE_RCFILE ?= config/coveragerc
COMPOSE_PROJECT_DIR ?= .
COMPOSE_FILE_BASE ?= infra/docker-compose.yml
COMPOSE_FILE_OVERRIDE ?= infra/docker-compose.override.yml
COMPOSE_FILES = -f $(COMPOSE_FILE_BASE) $(if $(wildcard $(COMPOSE_FILE_OVERRIDE)),-f $(COMPOSE_FILE_OVERRIDE))
DOCKER_COMPOSE = docker compose --project-directory $(COMPOSE_PROJECT_DIR) $(COMPOSE_FILES)

setup:
	pipx install pre-commit || pip install pre-commit
	pre-commit install --config $(PRE_COMMIT_CONFIG)

dev-up:
	$(DOCKER_COMPOSE) up -d postgres redis
	$(DOCKER_COMPOSE) up -d --build auth_service user_service

dev-down:
	$(DOCKER_COMPOSE) down -v

native-up:
	./scripts/dev/native_up.sh

native-down:
	./scripts/dev/native_down.sh

demo-up:
	$(DOCKER_COMPOSE) up -d postgres redis
	until $(DOCKER_COMPOSE) exec -T postgres pg_isready -U trading -d trading >/dev/null 2>&1; do \
	        echo "Waiting for postgres to be ready..."; \
	        sleep 1; \
	done
	$(DOCKER_COMPOSE) run --rm db_migrations
	$(DOCKER_COMPOSE) up -d --build auth_service user_service billing_service streaming streaming_gateway market_data \
	order_router algo_engine reports alert_engine notification_service inplay web_dashboard \
	prometheus grafana

demo-down:
	$(DOCKER_COMPOSE) down -v

lint:
	pre-commit run -a --config $(PRE_COMMIT_CONFIG)

test:
	python -m pip install -r $(REQUIREMENTS_DEV)
	python -m pip install -r requirements/services.txt
	python -m pip install -r requirements/services-dev.txt
	python -m coverage --rcfile $(COVERAGE_RCFILE) erase
	python -m coverage --rcfile $(COVERAGE_RCFILE) run -m pytest -m "not slow"
	python -m coverage --rcfile $(COVERAGE_RCFILE) xml
	python -m coverage --rcfile $(COVERAGE_RCFILE) html

e2e:
	pwsh -NoProfile -File ./scripts/e2e/auth_e2e.ps1

e2e-sh:
	bash ./scripts/e2e/auth_e2e.sh

web_dashboard-e2e:
	python -m playwright install --with-deps chromium firefox
	python -m pytest services/web_dashboard/tests/e2e

fix-makefile:
	@python scripts/dev/fix_make_tabs.py Makefile

# lance bootstrap dans le conteneur (robuste)
demo-bootstrap:
	$(DOCKER_COMPOSE) exec \
		-e BOOTSTRAP_AUTH_URL=http://auth_service:8000 \
		-e BOOTSTRAP_USER_URL=http://user_service:8000 \
		-e BOOTSTRAP_ALGO_URL=http://algo_engine:8000 \
		-e BOOTSTRAP_ORDER_ROUTER_URL=http://order_router:8000 \
		-e BOOTSTRAP_REPORTS_URL=http://reports:8000 \
		-e BOOTSTRAP_BILLING_URL=http://billing_service:8000 \
		-e BOOTSTRAP_DASHBOARD_URL=http://web_dashboard:8000 \
		-e BOOTSTRAP_STREAMING_URL=http://streaming:8000 \
		auth_service python /app/scripts/dev/bootstrap_demo.py BTCUSDT 0.25 --order-type market

migrate-generate:
	@if [ -z "$(message)" ]; then \
	echo "Usage: make migrate-generate message=\"Add new table\""; \
	exit 1; \
	fi
	ALEMBIC_DATABASE_URL=$(ALEMBIC_DATABASE_URL) alembic -c $(ALEMBIC_CONFIG) revision --autogenerate -m "$(message)"

migrate-up:
	ALEMBIC_DATABASE_URL=$(ALEMBIC_DATABASE_URL) alembic -c $(ALEMBIC_CONFIG) upgrade $(REVISION)

migrate-down:
	ALEMBIC_DATABASE_URL=$(ALEMBIC_DATABASE_URL) alembic -c $(ALEMBIC_CONFIG) downgrade $(DOWN_REVISION)
