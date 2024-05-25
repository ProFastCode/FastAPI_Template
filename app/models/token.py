"""
Token Model
"""

from pydantic import BaseModel, Field


class AuthToken(BaseModel):
    token: str = Field(
        description='Необходим для получения парных токенов, действует 15 мин.'
    )


class AccessToken(BaseModel):
    token: str = Field(
        description='Необходим для запросов к API, действует 2 часа.'
    )


class RefreshToken(BaseModel):
    token: str = Field(
        description='Необходим для получения нового токена доступа, действует 24 часа.'
    )


class PairTokens(BaseModel):
    access: AccessToken = Field()
    refresh: RefreshToken = Field()
