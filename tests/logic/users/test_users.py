from app.logic.logic import Logic
from app.models.auth import AccessToken
from app.models.users import UserCreate


async def test_create(logic: Logic, user_create: UserCreate):
    user = await logic.users.create(user_create)
    assert user is not None


async def test_retrieve(logic: Logic, access_token: AccessToken):
    user = await logic.users.retrieve_by_token(access_token.token)
    assert user is not None


async def test_delete(logic: Logic, access_token: AccessToken):
    await logic.users.delete_by_token(access_token.token)
