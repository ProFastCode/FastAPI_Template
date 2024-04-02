"""
Schemas Users
"""

from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    class Config:
        from_attributes = True


class EmailUser(BaseUser):
    email: EmailStr = Field(examples=["fast.code.auth@gmail.com"])


class PasswordUser(BaseUser):
    password: str = Field(examples=["12345"])


class GetUser(EmailUser):
    id: int = Field(examples=[0])


class NewUser(PasswordUser, EmailUser):
    pass


class AuthUser(PasswordUser, EmailUser):
    pass
