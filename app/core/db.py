from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app import repositories as repos
from app.core.settings import settings


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(
        self, engine: AsyncEngine | None = None, session: AsyncSession | None = None
    ) -> None:
        if not hasattr(self, "initialized"):
            self.engine = engine
            self.session = session
            self.initialized = True

    async def __set_async_engine(self) -> None:
        if self.engine is None:
            self.engine = create_async_engine(
                settings.pg_dsn.unicode_string(), echo=False, future=True
            )

    async def __set_async_session(self) -> None:
        if self.session is None:
            self.session = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )()

    async def __set_repositories(self) -> None:
        if self.session is not None:
            self.user = repos.UserRepo(session=self.session)

    async def __aenter__(self):
        await self.__set_async_engine()
        await self.__set_async_session()
        await self.__set_repositories()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session is not None:
            await self.session.close()
