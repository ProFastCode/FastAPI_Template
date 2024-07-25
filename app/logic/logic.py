from contextlib import asynccontextmanager
from typing import AsyncGenerator, Self

from app.core.db import Database

from .auth import Auth
from .security import Security
from .users import Users


class Logic:
    def __init__(self, db: Database):
        self.db = db
        self.security = Security()
        self.users = Users(self)
        self.auth = Auth(self)

    @classmethod
    @asynccontextmanager
    async def create(cls) -> AsyncGenerator[Self, None]:
        async with Database() as db:
            yield cls(db)
