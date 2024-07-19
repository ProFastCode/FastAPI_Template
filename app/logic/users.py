from typing import TYPE_CHECKING

from app.core import exps
from app.models.token import AccessToken
from app.models.user import User


if TYPE_CHECKING:
    from app.logic import Logic


class Users:
    def __init__(self, logic: "Logic"):
        self.logic = logic

    async def create(self, email: str, password: str) -> User | None:
        if await self.logic.db.user.retrieve_by_email(email):
            raise exps.USER_EXISTS

        password_hash = self.logic.security.pwd.hashpwd(password)
        model = User(email=email, password=password_hash)
        user = await self.logic.db.user.create(model)
        return user

    async def generate_token(self, email: str, password: str) -> AccessToken | None:
        if user := await self.logic.db.user.retrieve_by_email(email):
            if not self.logic.security.pwd.checkpwd(password, user.password):
                raise exps.USER_IS_CORRECT
            access_token = self.logic.security.jwt.encode_token(
                {"id": user.id}, 1440)
            return AccessToken(token=access_token)
        raise exps.USER_NOT_FOUND

    async def retrieve_by_token(self, token: str) -> User | None:
        if payload := self.logic.security.jwt.decode_token(token):
            if not (
                user := await self.logic.db.user.retrieve_one(ident=payload.get("id"))
            ):
                raise exps.USER_NOT_FOUND
            else:
                return user
