"""
Token Model
"""

from pydantic import BaseModel, Field


class AuthToken(BaseModel):
    token: str = Field(
        description='Необходим для получения пары токенов, действует 15 мин.'
    )


class PairTokens(BaseModel):
    access: str = Field(
        None, description='Необходим для запросов к API, действует 2 часа.'
    )
    refresh: str = Field(
        None,
        description='Необходим для получения нового токена доступа, действует 24 часа.',
    )
