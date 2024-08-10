from app.logic.logic import Logic
from app.models.users import UserCreate


async def test_hashpwd(hashpwd: str):
    assert hashpwd is not None


async def test_checkpwd(logic: Logic, hashpwd: str, user_create: UserCreate):
    data = logic.security.pwd.checkpwd(user_create.password, hashpwd)
    assert data is not None
