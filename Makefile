.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  dev		Start the app"
	@echo "  ref		Reformat code"
	@echo "  migrate		Alembic migrate database"
	@echo "  generate		Alembic generate database"

.PHONY: ref
ref:
	poetry run ruff ./app --fix && poetry run black ./app

.PHONY: dev
dev:
	uvicorn app:app --reload --access-log --log-level debug


.PHONY: generate
generate:
	poetry run alembic revision --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head