from typing import TYPE_CHECKING

from app.core import exps
from app.models.user import User

from .auth import Auth

if TYPE_CHECKING:
    from app.logic import Logic


class Users:
    def __init__(self, logic: "Logic"):
        self.logic = logic
        self.auth = Auth(self.logic)

    async def create(self, email: str, password: str) -> User | None:
        if await self.logic.db.user.retrieve_by_email(email):
            raise exps.UserExistsException()

        password_hash = self.logic.security.pwd.hashpwd(password)
        model = User(email=email, password=password_hash)
        user = await self.logic.db.user.create(model)
        return user

    async def retrieve_by_token(self, token: str) -> User | None:
        if payload := self.logic.security.jwt.decode_token(token):
            if not (
                user := await self.logic.db.user.retrieve_one(ident=payload.get("id"))
            ):
                raise exps.UserNotFoundException()
            else:
                return user
