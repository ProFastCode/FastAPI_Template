import datetime as dt
import uuid

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    pass


class IDModel(BaseModel):
    id: int = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )


class UUIDModel(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampModel(BaseModel):
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    updated_at: dt.datetime | None = Field(
        default_factory=dt.datetime.now,
        sa_column_kwargs={"onupdate": dt.datetime.now},
    )
