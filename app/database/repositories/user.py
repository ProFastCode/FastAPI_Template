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
        email: str,
        password: str,
    ) -> models.User:
        model = models.User()
        model.email = email
        model.password = password

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_email(
        self, email: str
    ) -> models.User | None:
        where_clauses = [self.type_model.email == email]
        entry = await self.get(where_clauses=where_clauses)
        return entry
