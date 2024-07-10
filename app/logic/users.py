from app.core import exps
from app.core.db import Database
from app.core.security import Security
from app.models.token import AccessToken
from app.models.user import User


class Users:
    def __init__(self, db: Database, security: Security):
        self.db = db
        self.security = security

    async def create(self, email: str, password: str) -> User | None:
        if await self.db.user.retrieve_by_email(email):
            raise exps.USER_EXISTS

        password_hash = self.security.pwd.hashpwd(password)
        model = User(email=email, password=password_hash)
        user = await self.db.user.create(model)
        return user

    async def generate_token(
        self, email: str, password: str
    ) -> AccessToken | None:
        if user := await self.db.user.retrieve_by_email(email):
            if not self.security.pwd.checkpwd(password, user.password):
                raise exps.USER_IS_CORRECT
            access_token = self.security.jwt.encode_token(
                {'id': user.id}, 1440
            )
            return AccessToken(token=access_token)
        raise exps.USER_NOT_FOUND

    async def retrieve_by_token(self, token: str) -> User | None:
        if payload := self.security.jwt.decode_token(token):
            if not (
                user := await self.db.user.retrieve_one(
                    ident=payload.get('id')
                )
            ):
                raise exps.USER_NOT_FOUND
            else:
                return user
