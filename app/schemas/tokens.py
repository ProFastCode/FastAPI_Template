"""
Schemas Tokens
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    class Config:
        from_attributes = True


class AuthToken(Token):
    auth_token: str = Field(
        examples=["auth_token"],
        description="Необходим для получения пары-токенов, действует 15мин.",
    )


class LongToken(Token):
    long_token: str = Field(
        examples=["long_token"],
        description="Необходим для получения нового короткого токена, действует 1год.",
    )


class ShortToken(Token):
    short_token: str = Field(
        examples=["short_token"],
        description="Необходим для запросов к API, действует 2часа.",
    )


class PairTokens(LongToken, ShortToken):
    pass
