"""
Schemas Users
"""

from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field("username", title="Username")

    class Config:
        from_attributes = True


class UserGet(User):
    id: int = Field(0, title="User ID")


class UserNew(User):
    password: str = Field("password", title="Password")
