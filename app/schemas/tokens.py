"""
Schemas Tokens
"""

from pydantic import ConfigDict, BaseModel, Field


class BaseToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuthToken(BaseToken):
    auth_token: str = Field(
        examples=["auth_token"],
        description="Необходим для получения пары-токенов, действует 15мин.",
    )


class LongToken(BaseToken):
    long_token: str = Field(
        examples=["long_token"],
        description="Необходим для получения нового короткого токена, действует 1год.",
    )


class ShortToken(BaseToken):
    short_token: str = Field(
        examples=["short_token"],
        description="Необходим для запросов к API, действует 2часа.",
    )


class PairTokens(LongToken, ShortToken):
    pass
