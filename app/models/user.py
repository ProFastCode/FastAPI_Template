"""
User Model
"""

from sqlmodel import Field, SQLModel

from .base import Base


class UserBase(SQLModel):
    email: str = Field()


class UserRead(Base, UserBase):
    pass


class UserCreate(UserBase):
    password: str = Field()


class User(Base, UserBase, table=True):
    password: str = Field()
    staff: bool = Field(False)
