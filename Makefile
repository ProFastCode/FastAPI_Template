.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  dev		Start the app"
	@echo "  ref		Reformat code"
	@echo "  req		pyproject.toml >> requirements.txt"
	@echo "  test	 	 Start the pytest"
	@echo "  migrate		Alembic migrate database"
	@echo "  generate	 	 Alembic generate database"


.PHONY:	blue
blue:
	poetry run blue app/

.PHONY: isort
isort:
	poetry run isort app/

.PHONY: ref
ref: blue isort

.PHONY: dev
dev:
	poetry run fastapi dev app

.PHONY: req
req:
	poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > requirements.txt

.PHONY: test
test:
	poetry run pytest tests

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: generate
generate:
	poetry run alembic revision --autogenerate
