from app import logic
from app.core.db import Database
from app.core.security import Security


class Logic:
    def __init__(self, db: Database, security: Security):
        self.users = logic.Users(db, security)


__all__ = ['Logic']
