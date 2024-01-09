"""
Схемы для пользователя.
"""

from pydantic import BaseModel


class UserScheme(BaseModel):
    """
    Схема, которую возвращает бэк.
    """
    id: int = 0
    email: str = "email"

    class Config:
        from_attributes = True


class UserSchemeAdd(BaseModel):
    """
    Схема создания пользователя.
    """
    email: str = "email"
    password: str = "password"


class UserTokenScheme(BaseModel):
    """
    Схема токена пользователя.
    """
    access_token: str
    token_type: str = "Bearer"

    class Config:
        populate_by_name = True
