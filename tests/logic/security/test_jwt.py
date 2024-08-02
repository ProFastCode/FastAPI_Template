import pytest
import pytest_asyncio

from app.logic.logic import Logic


@pytest_asyncio.fixture(scope="function")
async def token(logic: Logic) -> str:
    return logic.security.jwt.encode_token({}, 1)


@pytest.mark.asyncio
async def test_encode(token: str):
    assert token is not None


@pytest.mark.asyncio
async def test_decode(logic: Logic, token: str):
    data = logic.security.jwt.decode_token(token)
    assert data is not None
