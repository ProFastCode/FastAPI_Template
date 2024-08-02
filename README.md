# FastAPI

## Create a `.env` file based on `.env.dist` and make all the necessary customizations

### To run the application in a docker container, run the command

`docker-compose up -d`

### To run the application without a docker container, complete follow these steps

1. Install dependencies.

    `poetry install` or `pip install -r requirements.txt`
2. Run application.

    `poetry run fastapi dev app` or `make dev`

### Make documentation

`make help`
