from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.db import Database

from .auth import Auth
from .security import Security
from .user import User


class Logic:
    def __init__(self, db: Database):
        self.db = db
        self.auth = Auth(self)
        self.user = User(self)
        self.security = Security()

    @classmethod
    @asynccontextmanager
    async def create(cls) -> AsyncGenerator["Logic", None]:
        async with Database() as db:
            yield cls(db)
