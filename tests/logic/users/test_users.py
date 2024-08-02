import pytest
import pytest_asyncio

from app.logic.logic import Logic
from app.models.auth import AccessToken
from app.models.users import UserCreate


@pytest_asyncio.fixture(scope="function")
async def user_create() -> UserCreate:
    return UserCreate(email="email@email.email", password="password")


@pytest_asyncio.fixture(scope="function")
async def access_token(logic: Logic, user_create: UserCreate) -> AccessToken | None:
    return await logic.auth.generate_token(user_create)


@pytest.mark.asyncio
async def test_create(logic: Logic, user_create: UserCreate):
    user = await logic.users.create(user_create)
    assert user is not None


@pytest.mark.asyncio
async def test_retrieve(logic: Logic, access_token: AccessToken):
    user = await logic.users.retrieve_by_token(access_token.token)
    assert user is not None
