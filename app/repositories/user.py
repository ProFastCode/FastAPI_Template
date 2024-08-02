"""
User Repository
"""

from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.users import User

from .base import Repository


class UserRepo(Repository[User]):
    model: User

    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def retrieve_by_email(self, email: str) -> Optional[User]:
        return await self.retrieve_one(
            where_clauses=[self.model.email == email]
        )
