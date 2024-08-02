from typing import AsyncGenerator

import pytest_asyncio

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from app.logic import Logic
from app.core.db import Database
from app.models.auth import AccessToken
from app.models.users import UserCreate


engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator[Database, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with Database(engine=engine) as db:
        yield db


@pytest_asyncio.fixture(scope="function")
async def logic(db: Database) -> Logic:
    return Logic(db)


@pytest_asyncio.fixture(scope="function")
async def user_create_model() -> UserCreate:
    return UserCreate(email="email@email.email", password="password")


@pytest_asyncio.fixture(scope="function")
async def token(logic: Logic) -> str:
    return logic.security.jwt.encode_token({}, 1)


@pytest_asyncio.fixture(scope="function")
async def access_token(
    logic: Logic, user_create_model: UserCreate
) -> AccessToken | None:
    return await logic.auth.generate_token(user_create_model)
