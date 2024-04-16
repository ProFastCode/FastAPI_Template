"""
Token Model
"""

from sqlmodel import Field, SQLModel


class TokenBase(SQLModel):
    pass


class AuthToken(TokenBase):
    auth_token: str = Field(
        description="Необходим для получения пары-токенов, действует 15мин.",
    )


class LongToken(TokenBase):
    long_token: str = Field(
        description="Необходим для получения нового короткого токена, действует 1год.",
    )


class ShortToken(TokenBase):
    short_token: str = Field(
        description="Необходим для запросов к API, действует 2часа.",
    )


class PairTokens(LongToken, ShortToken):
    pass
