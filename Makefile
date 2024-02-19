.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Start the app"
	@echo "  lint		Reformat code"
	@echo "  migrate		Alembic migrate database"
	@echo "  generate		Alembic generate database"

.PHONY: lint
lint:
	poetry run ruff ./app --fix && poetry run black ./app

.PHONY: run
run:
	poetry run python -m app

.PHONY: generate
generate:
	poetry run alembic revision --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head