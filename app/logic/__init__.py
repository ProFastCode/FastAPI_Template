from typing import Self

from app.core.db import Database

from .security import Security
from .users import Users


class Logic:
    def __init__(self, db: Database):
        self.db = db
        self.security = Security()
        self.users = Users(self)

    @classmethod
    async def create(cls) -> Self:
        async with Database() as db:
            return cls(db)


__all__ = ['Logic']
