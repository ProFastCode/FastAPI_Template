# FastAPI

## File Structure
```
.
├── __init__.py
├── api
│   ├── __init__.py
│   ├── deps.py
│   └── v1
│       ├── __init__.py
│       ├── auth
│       │   ├── __init__.py
│       │   └── token.py
│       └── users
│           ├── __init__.py
│           ├── create.py
│           └── retrieve.py
├── core
│   ├── __init__.py
│   ├── db.py
│   ├── exps.py
│   └── settings.py
├── logic
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── logic.py
│   ├── security
│   │   ├── __init__.py
│   │   ├── jwt.py
│   │   ├── pwd.py
│   │   └── security.py
│   └── users
│       ├── __init__.py
│       └── users.py
├── models
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── token.py
│   ├── base.py
│   ├── types
│   │   ├── __init__.py
│   │   └── unix.py
│   └── users
│       ├── __init__.py
│       └── user.py
└── repositories
    ├── __init__.py
    ├── base.py
    └── user.py

14 directories, 34 files
```

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
