from typing import AsyncGenerator

import pytest

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from app.logic import Logic
from app.core.db import Database
from app.models.auth import AccessToken
from app.models.users import UserCreate


engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)


@pytest.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[Database, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with Database(engine=engine) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def logic(db: Database) -> Logic:
    return Logic(db)


@pytest.fixture(scope="function")
async def user_create() -> UserCreate:
    return UserCreate(email="email@email.email", password="password")


@pytest.fixture(scope="function")
async def token(logic: Logic) -> str:
    return logic.security.jwt.encode_token({}, 1)


@pytest.fixture(scope="function")
async def access_token(logic: Logic, user_create: UserCreate) -> AccessToken | None:
    return await logic.auth.generate_token(user_create)


@pytest.fixture(scope="function")
async def hashpwd(logic: Logic, user_create: UserCreate) -> str | None:
    return logic.security.pwd.hashpwd(user_create.password)
