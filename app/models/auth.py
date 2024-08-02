"""
Token Model
"""

from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    token: str = Field(
        None, description='Необходим для запросов к API, действует 24 часа.'
    )
