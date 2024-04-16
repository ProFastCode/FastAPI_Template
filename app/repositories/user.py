"""
User Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class UserRepo(Repository[models.User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.User, session=session)

    async def new(self, email: str, password: str) -> models.User:
        model = models.User(email=email, password=password)
        self.session.add(model)
        await self.session.flush()
        return model

    async def get_by_email(self, email: str) -> models.User | None:
        return await self.get_by_where_clauses([self.type_model.email == email])
