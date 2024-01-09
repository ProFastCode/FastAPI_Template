"""
Репозиторий пользователя.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models import User


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        email: str | None = None,
        password: str | None = None,
    ) -> User:
        new_user = await self.session.merge(
            User(
                email=email,
                password=password,
            )
        )
        return new_user

    async def get_by_email(self, email: str) -> User:
        user = await self.get_by_where(User.email == email)
        return user
