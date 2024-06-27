import datetime as dt
import uuid
from functools import partial

from sqlalchemy.types import BigInteger, TypeDecorator
from sqlmodel import Field, SQLModel


datetime_utc_now = partial(dt.datetime.now, tz=dt.UTC)


class UnixType(TypeDecorator):
    impl = BigInteger
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(BigInteger())

    def process_bind_param(
        self, value: dt.date | dt.datetime | str | None, dialect
    ) -> int | None:
        if isinstance(value, dt.datetime):
            return int(value.timestamp())
        elif isinstance(value, dt.date):
            return int(dt.datetime.combine(value, dt.time.min).timestamp())
        elif isinstance(value, str):
            return int(dt.datetime.fromisoformat(value).timestamp())

    def process_result_value(self, value: int | None, dialect) -> dt.datetime | None:
        if isinstance(value, int):
            return dt.datetime.fromtimestamp(value, dt.UTC)


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
    created_at: int | str | dt.datetime = Field(
        default_factory=datetime_utc_now,
        sa_type=UnixType,
        nullable=False,
    )
    updated_at: int | str | dt.datetime | None = Field(
        default_factory=datetime_utc_now,
        sa_type=UnixType,
        nullable=True,
        sa_column_kwargs={"onupdate": datetime_utc_now},
    )

    class Config(SQLModel.Config):
        arbitrary_types_allowed = True
