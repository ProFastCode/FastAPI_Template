from fastapi import status

from app import schemas
from app.core import security
from ..abstract import AbstractUseCase


class AuthUseCase(AbstractUseCase):
    async def execute(self, data: schemas.users.AuthUser):
        if not (user := await self.db.user.get_by_email(data.email)):
            self.exp(status.HTTP_401_UNAUTHORIZED, "A user not yet been registered")

        if not security.password_manager.verify_password(data.password, user.password):
            self.exp(status.HTTP_401_UNAUTHORIZED, "Incorrect password")

        auth_token = security.token_manager.create_auth_token({"id": user.id})
        await self.db.user_activity.new(
            user_id=user.id,
            action="new_auth_token",
            comment="Новый токен аутентификации",
            user_agent=self.user_agent,
            ip=self.host,
        )
        await self.db.session.commit()
        return schemas.tokens.AuthToken(auth_token=auth_token)
