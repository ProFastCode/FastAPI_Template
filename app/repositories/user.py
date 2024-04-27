"""
User Repository
"""

import sqlmodel as sm
from sqlmodel.ext.asyncio.session import AsyncSession

from .abstract import Repository
from ..models import User


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        stmt = sm.select(self.type_model).where(self.type_model.email == email)
        result = await self.session.exec(stmt)
        return result.one_or_none()
