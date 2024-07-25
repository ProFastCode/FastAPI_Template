from typing import TYPE_CHECKING

from app.core import exps
from app.models.users.user import User, UserCreate

if TYPE_CHECKING:
    from app.logic import Logic


class Users:
    def __init__(self, logic: 'Logic'):
        self.logic = logic

    async def create(self, model: UserCreate) -> User | None:
        if await self.logic.db.user.retrieve_by_email(model.email):
            raise exps.UserExistsException()

        model.password = self.logic.security.pwd.hashpwd(model.password)
        user = await self.logic.db.user.create(model)
        return user

    async def retrieve_by_token(self, token: str) -> User | None:
        payload = self.logic.security.jwt.decode_token(token)
        if not (
            user := await self.logic.db.user.retrieve_one(
                ident=payload.get('id')
            )
        ):
            raise exps.UserNotFoundException()
        return user
