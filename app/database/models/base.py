"""
Base Model
"""

from datetime import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, as_declarative

metadata = sa.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


@as_declarative(metadata=metadata)
class Base:
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False

    id: Mapped[int] = mapped_column(sa.Integer, autoincrement=True, primary_key=True)
    create_at: Mapped[str] = mapped_column(sa.DateTime, unique=False, default=dt.now())
    update_at: Mapped[str] = mapped_column(
        sa.DateTime, unique=False, onupdate=dt.now(), default=dt.now()
    )

    def __repr__(self):
        return f"{__class__.__name__}({self.id=})"
