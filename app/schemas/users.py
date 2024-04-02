"""
Schemas Users
"""

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    class Config:
        from_attributes = True


class UserEmail(User):
    email: EmailStr = Field(examples=["fast.code.auth@gmail.com"])


class UserPassword(User):
    password: str = Field(examples=["12345"])


class UserGet(UserEmail):
    id: int = Field(examples=[0])


class UserNew(UserPassword, UserEmail):
    pass
