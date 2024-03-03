"""
User Repository
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
        model = models.User()
        model.username = username
        model.password = password

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_username(self, username: str, password: str | None = None) -> models.User | None:
        where_clause = [self.type_model.username == username]
        if password:
            where_clause.append(self.type_model.password == password)
        entry = await self.get_by_where(where_clause)
        return entry
