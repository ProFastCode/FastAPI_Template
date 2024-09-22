from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models import user as user_models

from .base import Repository


class UserRepo(Repository[user_models.User]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=user_models.User, session_maker=session_maker)

    async def retrieve_by_email(self, email: str) -> user_models.User | None:
        return await self.retrieve_one(
            where_clauses=[self.model.email == email]
        )
