"""
User Model
"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    staff: Mapped[bool] = mapped_column(sa.Boolean, unique=False, default=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)

    def __repr__(self):
        return f"{__class__.__name__}({self.id=}, {self.staff}, {self.email=})"
