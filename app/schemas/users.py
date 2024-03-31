"""
Schemas Users
"""

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    email: EmailStr = Field(examples=["fast.code.auth@gmail.com"])

    class Config:
        from_attributes = True


class UserGet(User):
    id: int = Field(examples=[0])


class UserNew(User):
    password: str = Field(examples=["12345"])
