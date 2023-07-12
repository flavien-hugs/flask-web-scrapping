MANAGE := FLASK_APP=runserver.py

ifneq (,$(wildcard ./.flaskenv))
    include ./.flaskenv
    export
endif

.PHONY: help
help: ## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install or update dependencies
	pip install -r env/dev.txt

.PHONY: run
run: ## Run
	docker compose up -d --build

initdb: ## Init and migrate database
	docker compose exec web.yimba.io python runserver.py flask db init
	docker compose exec web.yimba.io python runserver.py flask init_db

migrate: ## Init and migrate database
	docker compose exec web.yimba.io python runserver.py flask db migrate -m 'Intial Migration'

upgrade: ## Apply the upgrade to the database
	docker compose exec web.yimba.io python runserver.py flask db upgrade

.PHONY: logs
logs: ## View logs from one/all containers
	docker compose logs -f $(s)

.PHONY: down
down: ## Stop the services, remove containers and networks
	docker compose down -v

.PHONY: destroy-all
destroy-all: ## destroy one/all images
	docker rmi -f $(docker images -a -q)
