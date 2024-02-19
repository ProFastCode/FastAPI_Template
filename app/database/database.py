from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.core import settings
from . import repositories as repos

engine: AsyncEngine = create_async_engine(
    settings.pg_dns, echo=False, pool_pre_ping=True
)


async def new_session() -> AsyncSession:
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        return session


class Database:
    def __init__(
        self,
        session: Optional[AsyncSession] = None,
    ):
        self.session = session

        self.user = repos.UserRepo(session=session)
