"""
Schemas Users
"""

from pydantic import ConfigDict, BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StaffUser(BaseUser):
    staff: bool = Field(examples=[False])


class EmailUser(BaseUser):
    email: EmailStr = Field(examples=["fast.code.auth@gmail.com"])


class PasswordUser(BaseUser):
    password: str = Field(examples=["12345"])


class GetUser(EmailUser, StaffUser):
    id: int = Field(examples=[0])


class NewUser(PasswordUser, EmailUser):
    pass


class AuthUser(PasswordUser, EmailUser):
    pass
