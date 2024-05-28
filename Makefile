.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  dev		Start the app"
	@echo "  ref		Reformat code"
	@echo "  req		pyproject.toml >> requirements.txt"
	@echo "  migrate		Alembic migrate database"
	@echo "  generate		Alembic generate database"


.PHONY:	blue
blue:
	poetry run blue app/

.PHONY: isort
isort:
	poetry run isort app/

.PHONY: ruff
ruff:
	poetry run ruff check app/ --fix --respect-gitignore

.PHONY: ref
ref: blue isort ruff

.PHONY: dev
dev:
	poetry run fastapi dev app

.PHONY: req
req:
	poetry export -f requirements.txt --output requirements.txt

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: generate
generate:
	poetry run alembic revision --autogenerate
