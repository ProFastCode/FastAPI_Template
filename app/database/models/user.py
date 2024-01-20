"""
Модель пользователя.
"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)

    def __repr__(self):
        return f"User:{self.id=}"
