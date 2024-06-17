"""
User Model
"""

from sqlmodel import Field, SQLModel

from .base import IDModel


class UserBase(SQLModel):
    email: str = Field()
    password: str = Field()


class User(IDModel, UserBase, table=True):
    pass


class UserCreate(UserBase):
    pass


class UserRead(IDModel):
    email: str = Field()
