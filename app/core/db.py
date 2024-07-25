"""
Database
"""

from typing import Self

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app import repositories as repos
from app.core.settings import settings


class Database:
    def __init__(
        self,
        engine: AsyncEngine | None = None,
        session: AsyncSession | None = None,
    ) -> None:
        self.__engine = engine
        self.__session = session

    async def __set_async_engine(self) -> None:
        if self.__engine is None:
            self.__engine = create_async_engine(
                settings.pg_dsn.unicode_string(), echo=False, future=True
            )

    async def __set_async_session(self) -> None:
        if self.__session is None:
            self.__session = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.__engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )()

    async def __set_repositories(self) -> None:
        if self.__session is not None:
            self.user = repos.UserRepo(session=self.__session)

    async def __aenter__(self) -> Self:
        await self.__set_async_engine()
        await self.__set_async_session()
        await self.__set_repositories()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.__session is not None:
            await self.__session.commit()
            await self.__session.close()
