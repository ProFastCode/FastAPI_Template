"""
User Model
"""

from sqlmodel import Field

from .base import BaseModel, UUIDModel, TimestampModel


class UserBase(BaseModel):
    email: str = Field()


class User(UUIDModel, TimestampModel, UserBase, table=True):
    password: str = Field()
    is_superuser: bool = Field(False)


class UserCreate(UserBase):
    password: str = Field()


class UserRead(UUIDModel, TimestampModel, UserBase):
    is_superuser: bool = Field()
