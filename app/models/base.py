import datetime as dt
import uuid
from functools import partial

from sqlalchemy.types import BigInteger, TypeDecorator
from sqlmodel import Field, SQLModel

datetime_utcnow = partial(dt.datetime.now, tz=dt.UTC)


class UnixType(TypeDecorator):
    impl = BigInteger
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(BigInteger())

    def process_bind_param(self, value, dialect) -> int | None:
        if isinstance(value, (dt.datetime, dt.date)):
            return int(value.timestamp())
        return value

    def process_result_value(self, value, dialect) -> dt:
        if isinstance(value, int):
            return dt.datetime.fromtimestamp(value, dt.UTC)
        return value


class IDModel(SQLModel):
    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )


class UUIDModel(SQLModel):
    external_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, nullable=False, unique=True
    )


class TimestampModel(SQLModel):
    created_at: int | dt.datetime = Field(
        default_factory=datetime_utcnow,
        sa_type=UnixType,
        nullable=False,
    )
    updated_at: int | dt.datetime | None = Field(
        default_factory=datetime_utcnow,
        sa_type=UnixType,
        nullable=True,
        sa_column_kwargs={'onupdate': datetime_utcnow},
    )

    class Config:
        arbitrary_types_allowed = True
