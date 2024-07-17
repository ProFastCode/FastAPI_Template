from app.core.db import Database
from app.core.security import Security

from .users import Users


class Logic:
    def __init__(self, db: Database, security: Security):
        self.users = Users(db, security)


__all__ = ['Logic']
