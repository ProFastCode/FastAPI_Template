from typing import TYPE_CHECKING

from app.core import exps
from app.models import user as user_models

if TYPE_CHECKING:
    from app.logic import Logic


class User:
    def __init__(self, logic: "Logic"):
        self.logic = logic

    async def create(self, data: user_models.UserCreate) -> user_models.User | None:
        if await self.logic.db.user.retrieve_by_email(data.email):
            raise exps.UserExistsException()

        data.password = self.logic.security.pwd.hashpwd(data.password)
        user = await self.logic.db.user.create(data)
        return user

    async def retrieve_by_token(self, token: str) -> user_models.User | None:
        payload = self.logic.security.jwt.decode_token(token)
        if not (user := await self.logic.db.user.retrieve_one(ident=payload.get("id"))):
            raise exps.UserNotFoundException()
        return user
