"""
Abstract Repository
"""

import abc
import typing
from typing import Generic, TypeVar

import sqlalchemy as sa
import sqlmodel as sm
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models import Base

AbstractModel = TypeVar("AbstractModel", bound=Base)


class Repository(Generic[AbstractModel], metaclass=abc.ABCMeta):
    type_model: typing.Type[AbstractModel]
    session: AsyncSession

    def __init__(self, type_model: typing.Type[AbstractModel], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get_by_id(self, ident: int) -> typing.Optional[AbstractModel]:
        entry = await self.session.get(self.type_model, ident)
        return entry

    async def get_by_where_clauses(
        self, where_clauses: typing.List[sa.ClauseElement | bool]
    ) -> typing.Optional[AbstractModel]:
        result = await self.session.exec(
            sm.select(self.type_model).where(sm.and_(*where_clauses))
        )
        entry = result.one_or_none()
        return entry

    async def get_many(
        self,
        where_clauses: typing.List[sa.ColumnElement | bool] = None,
        limit: int = None,
        order_by: sa.ColumnElement = None,
    ) -> typing.Sequence[AbstractModel]:
        stmt = sm.select(self.type_model).limit(limit).order_by(order_by)
        if where_clauses:
            stmt = stmt.where(sm.and_(*where_clauses))
        results = await self.session.exec(stmt)
        return results.all()

    async def count(
        self, where_clauses: typing.List[sa.ClauseElement | bool] = None
    ) -> int:
        stmt = sm.select(sm.func.count()).select_from(self.type_model)
        if where_clauses:
            stmt = stmt.where(sm.and_(*where_clauses))
        result = await self.session.exec(stmt)
        return result.one()

    async def update_by_id(self, ident: int = None, **values) -> sa.Result:
        stmt = (
            sm.update(self.type_model)
            .values(**values)
            .where(sm.and_(self.type_model.id == ident))
        )
        return await self.session.execute(stmt)

    async def update_by_where_clauses(
        self, where_clauses: typing.List[sa.ClauseElement | bool] = None, **values
    ) -> sa.Result:
        stmt = (
            sm.update(self.type_model).values(**values).where(sm.and_(*where_clauses))
        )
        return await self.session.execute(stmt)

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None: ...
