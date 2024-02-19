"""
Репозиторий пользователя.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class UserRepo(Repository[models.User]):
    type_model: type[models.User]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.User, session=session)

    async def new(
        self,
        username: str,
        password: str,
    ) -> models.User:
        new_user = models.User()
        new_user.username = username
        new_user.password = password

        new_user = await self.session.merge(new_user)
        await self.session.flush()
        return new_user

    async def get_by_username(self, username: str) -> models.User | None:
        user = await self.get_by_where(self.type_model.username == username)
        return user
