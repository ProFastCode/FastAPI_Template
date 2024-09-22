from typing import Self

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app import repositories as repos
from app.core.settings import settings


class Database:
    user: repos.UserRepo

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        engine: AsyncEngine | None = None,
        session_maker: async_sessionmaker | None = None,
    ) -> None:
        if not hasattr(self, "initialized"):
            self.__engine = engine
            self.__session_maker = session_maker
            self.__initialized = True

    async def __set_async_engine(self) -> None:
        if self.__engine is None:
            self.__engine = create_async_engine(settings.postgres_dsn)

    async def __set_session_maker(self) -> None:
        if self.__session_maker is None:
            self.__session_maker = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.__engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

    async def __set_repositories(self) -> None:
        if self.__session_maker is not None:
            self.user = repos.UserRepo(self.__session_maker)

    async def __aenter__(self) -> Self:
        await self.__set_async_engine()
        await self.__set_session_maker()
        await self.__set_repositories()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.__engine is not None:
            await self.__engine.dispose()
