"""
User Model
"""

from sqlmodel import BigInteger, Field, SQLModel


class UserBase(SQLModel):
    id: int = Field(primary_key=True, unique=True, sa_type=BigInteger)
    username: str | None = Field(default=None)
    photo_url: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)


class User(UserBase, table=True):
    pass


class UserCreate(UserBase):
    hash: str = Field()
    auth_date: int = Field()


class UserRead(UserBase):
    pass
