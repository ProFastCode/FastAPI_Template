"""
User Repository
"""
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User

from .abstract import Repository


class UserRepo(Repository[User]):
    model: User

    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def retrieve_by_email(self, email: str) -> Optional[User]:
        return await self.retrieve_one(
            where_clauses=[self.model.email == email]
        )
