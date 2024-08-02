import datetime as dt
import uuid
from functools import partial

from sqlmodel import Field, SQLModel

from .types import UnixType

datetime_utc_now = partial(dt.datetime.now, tz=dt.UTC)


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
        sa_column_kwargs={'onupdate': datetime_utc_now},
    )
