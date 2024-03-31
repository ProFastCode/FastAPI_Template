"""
Schemas Tokens
"""

from pydantic import BaseModel, Field


class TokenAuth(BaseModel):
    token_auth: str = Field(
        examples=["token_auth"],
        description="Необходим для получения пары-токенов, действует 15мин.",
    )

    class Config:
        from_attributes = True


class TokenLong(BaseModel):
    token_long: str = Field(
        examples=["token_long"],
        description="Необходим для получения нового короткого токена, действует 1год.",
    )


class TokenShort(BaseModel):
    token_short: str = Field(
        examples=["token_short"],
        description="Необходим для запросов к API, действует 2часа.",
    )

    class Config:
        from_attributes = True


class TokenPair(TokenLong, TokenShort):
    pass
