from app.core.db import Database

from .users import Users
from .security import Security


class Logic:
    def __init__(self, db: Database):
        self.db = db
        self.security = Security()
        self.users = Users(self)

    @classmethod
    async def create(cls) -> "Logic":
        async with Database() as db:
            return cls(db)


__all__ = ["Logic"]
