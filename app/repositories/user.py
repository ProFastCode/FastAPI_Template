"""
User Repository
"""

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User

from .abstract import Repository


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
