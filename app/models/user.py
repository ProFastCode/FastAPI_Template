"""
User Model
"""

from sqlmodel import BigInteger, Field, SQLModel

from .base import IDModel


class UserBase(SQLModel):
    full_name: str = Field()
    photo_url: str = Field()
    telegram_id: int = Field(sa_type=BigInteger, index=True, unique=True)


class User(IDModel, UserBase, table=True):
    pass


class UserCreate(UserBase):
    pass


class UserRead(IDModel, UserBase):
    pass
