from fastapi import status

from app.core import security
from app import schemas
from ..abstract import AbstractUseCase


class RefreshUseCase(AbstractUseCase):
    async def execute(self, data: schemas.tokens.LongToken):
        payload = security.token_manager.decode_long_token(data.long_token)
        if not (user := await self.db.user.get(payload.get("id"))):
            self.exp(status.HTTP_401_UNAUTHORIZED, "User not found")

        short_token = security.token_manager.create_short_token(payload)
        await self.db.user_activity.new(
            user.id,
            "refresh_short_token",
            "Обновлён короткий токен",
            user_agent=self.user_agent,
            ip=self.host,
        )
        await self.db.session.commit()
        return schemas.tokens.ShortToken(short_token=short_token)
