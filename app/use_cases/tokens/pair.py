from fastapi import status

from app.core import security
from app import schemas
from ..abstract import AbstractUseCase


class PairUseCase(AbstractUseCase):
    async def execute(self, data: schemas.tokens.AuthToken):
        payload = security.token_manager.decode_auth_token(data.auth_token)
        if not (user := await self.db.user.get(payload.get("id"))):
            self.exp(status.HTTP_401_UNAUTHORIZED, "User not found")

        long_token = security.token_manager.create_long_token(payload)
        short_token = security.token_manager.create_short_token(payload)
        await self.db.user_activity.new(
            user_id=user.id,
            action="new_pair_tokens",
            comment="Новая пара токенов",
            user_agent=self.user_agent,
            ip=self.host,
        )
        await self.db.session.commit()
        return schemas.tokens.PairTokens(long_token=long_token, short_token=short_token)
