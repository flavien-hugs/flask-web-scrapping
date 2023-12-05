MANAGE := FLASK_APP=runserver.py

ifneq (,$(wildcard ./dotenv/*.env))
    include ./dotenv/*.env
    export
endif

COMPOSE_FILES := docker-compose.yaml
.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install or update dependencies
	pip install -r env/dev.txt

initdb: ## Init and create database
	$(MANAGE) flask db init && $(MANAGE) flask init_db

migrate: ## Generate an migration
	$(MANAGE) flask db migrate -m 'Intial Migration'

upgrade: ## Apply the upgrade to the database
	$(MANAGE) flask db upgrade

.PHONY: run
run: ## Run
	docker compose up -d --build

.PHONY: restart
restart: ## restart one/all containers
	docker compose restart $(s)

docker-initdb: ## Init and migrate database
	docker compose exec web.yimba.io python runserver.py flask db init
	docker compose exec web.yimba.io python runserver.py flask init_db

docker-migrate: ## Init and migrate database
	docker compose exec web.yimba.io python runserver.py flask db migrate -m 'Intial Migration'

docker-upgrade: ## Apply the upgrade to the database
	docker compose exec web.yimba.io python runserver.py flask db upgrade

.PHONY: logs
logs: ## View logs from one/all containers
	docker compose logs -f $(s)

.PHONY: down
down: ## Stop the services, remove containers and networks
	docker compose down -v

.PHONY: prune
prune: ## destroy one/all images
	docker system prune
	docker volume prune

.PHONY: test
test: ## Run the test
	coverage run -m pytest tests

.PHONY: report-test
report-test: ## Display coverage report
	coverage report -m
