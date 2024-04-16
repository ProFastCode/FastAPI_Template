import datetime as dt
from typing import Optional

from sqlmodel import Field, SQLModel


class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[dt.datetime] = Field(default_factory=dt.datetime.now)
    updated_at: Optional[dt.datetime] = Field(
        default_factory=dt.datetime.now,
        sa_column_kwargs={"onupdate": dt.datetime.now},
    )
