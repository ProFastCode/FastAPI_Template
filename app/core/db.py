"""
Database
"""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app import repositories as repos
from app.core.settings import settings


class Database:
    session: AsyncSession

    @classmethod
    def __get_async_engine(cls) -> AsyncEngine:
        return create_async_engine(
            settings.pg_dsn.unicode_string(), echo=False, future=True
        )

    @classmethod
    def __get_async_session(cls) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=cls.__get_async_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )

    def __set_repositories(self):
        self.user = repos.UserRepo(session=self.session)

    async def __aenter__(self):
        async with self.__get_async_session()() as session:
            self.session = session
        self.__set_repositories()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()
