"""
Token Model
"""

from sqlmodel import Field

from .base import BaseModel


class AuthToken(BaseModel):
    auth_token: str = Field(
        description="Необходим для получения пары-токенов, действует 15мин.",
    )


class LongToken(BaseModel):
    long_token: str = Field(
        description="Необходим для получения нового короткого токена, действует 1год.",
    )


class ShortToken(BaseModel):
    short_token: str = Field(
        description="Необходим для запросов к API, действует 2часа.",
    )


class PairTokens(LongToken, ShortToken):
    pass
