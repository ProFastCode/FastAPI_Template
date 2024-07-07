[Preview API](https://profastcode.github.io/FastAPI_Template/docs/)

## Настройка

#### Настройка происходит в файле .env его нет в репозитории, т.к. он конфиденциален, но я предоставил файл .env.dist создайте на его основе файл .env и проведите все необходимые настройки

## Документация по make командам

`make help` - Отображает команды и их описание.

`make ref` - Форматирует код.

`make dev` - Запускает приложение в режиме разработки.

`make req` - Обновляет зависимости в [requirements.txt](requirements.txt)

`make migrate` - Применяет все миграции с помощью alembic.

`make generate` - Генерирует новую миграцию с помощью alembic.
