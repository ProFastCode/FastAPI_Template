import pytest
import pytest_asyncio

from app.logic.logic import Logic
from app.models.users import UserCreate


@pytest_asyncio.fixture(scope="function")
async def hashpwd(logic: Logic, user_create_model: UserCreate):
    return logic.security.pwd.hashpwd(user_create_model.password)


@pytest.mark.asyncio
async def test_hashpwd(hashpwd: str):
    assert hashpwd is not None


@pytest.mark.asyncio
async def test_checkpwd(logic: Logic, hashpwd: str, user_create_model: UserCreate):
    data = logic.security.pwd.checkpwd(user_create_model.password, hashpwd)
    assert data is not None
