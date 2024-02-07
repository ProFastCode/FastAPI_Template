"""
Абстрактный репозиторий от которого наследуются остальные репозитории.
"""

import abc
from typing import Generic, TypeVar, Optional, List, Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar('AbstractModel')


class Repository(Generic[AbstractModel]):
    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause) -> AbstractModel | None:
        statement = sa.select(self.type_model).where(whereclause)
        return (await self.session.execute(statement)).unique().scalar_one_or_none()

    async def get_many(
            self, whereclause: Optional [List[Any]] = None, limit: Optional[int] = None, order_by=None
    ):
        statement = sa.select(self.type_model).limit(limit).order_by(order_by)
        if whereclause:
            statement = statement.where(sa.and_(*whereclause))
        return (await self.session.scalars(statement)).unique().all()

    async def delete(self, whereclause) -> None:
        statement = sa.delete(self.type_model).where(whereclause)
        await self.session.execute(statement)

    async def update(self, ident: int, **values):
        statement = sa.update(self.type_model).values(**values).where(self.type_model.id == ident)
        await self.session.execute(statement)

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        ...
