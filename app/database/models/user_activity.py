"""
User Activity Model
"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserActivity(Base):
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)
    action: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    comment: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
    user_agent: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    ip: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)

    def __repr__(self):
        return f"{__class__.__name__}({self.id=}, {self.action=}, {self.ip}, {self.user_agent=})"
