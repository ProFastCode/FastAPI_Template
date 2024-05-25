"""
Token Model
"""

from sqlmodel import Field, SQLModel


class AuthToken(SQLModel):
    auth_token: str = Field(
        description='Необходим для получения парных токенов, действует 15 мин.',
    )


class AccessToken(SQLModel):
    access_token: str = Field(
        description='Необходим для запросов к API, действует 2 часа.',
    )


class RefreshToken(SQLModel):
    refresh_token: str = Field(
        description='Необходим для получения нового токена доступа, действует 24 часа.',
    )


class PairTokens(AccessToken, RefreshToken):
    pass
