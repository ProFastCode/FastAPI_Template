"""
User Model
"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.core.structures import Role
from .base import Base


class User(Base):
    role: Mapped[int] = mapped_column(sa.Integer, unique=False, default=Role.USER)
    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)

    def __repr__(self):
        return f"{__class__.__name__}({self.id=}, {self.role=}, {self.email=})"
