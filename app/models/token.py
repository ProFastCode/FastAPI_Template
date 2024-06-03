"""
Token Model
"""

from pydantic import BaseModel, Field


class PairTokens(BaseModel):
    access: str = Field(description='Необходим для запросов к API, действует 2 часа.')
    refresh: str = Field(description='Необходим для получения нового токена доступа, действует 24 часа.')
