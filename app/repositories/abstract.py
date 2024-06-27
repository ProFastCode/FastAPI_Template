import abc

import sqlmodel as sm
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import (
    Any,
    Generic,
    List,
    NoReturn,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

AbstractModel = TypeVar("AbstractModel", bound=sm.SQLModel)


class Repository(Generic[AbstractModel], metaclass=abc.ABCMeta):
    def __init__(self, model: Type[AbstractModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, model: AbstractModel) -> AbstractModel:
        self.model.model_validate(model)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def retrieve_one(
        self,
        *,
        ident: Optional[int] = None,
        where_clauses: Optional[List[Optional[sm.DefaultClause]] | List[bool]] = None,
    ) -> Optional[AbstractModel]:
        if ident is not None:
            return await self.session.get(self.model, ident)
        stmt = sm.select(self.model)
        if where_clauses is not None:
            stmt = stmt.where(sm.and_(*where_clauses))
        entity = await self.session.exec(stmt)
        return entity.first()

    async def retrieve_many(
        self,
        where_clauses: Optional[List[Optional[sm.DefaultClause]] | List[bool]] = None,
        limit: Optional[int] = None,
        order_by: Optional[Any] = None,
    ) -> Optional[Sequence[AbstractModel]]:
        stmt = sm.select(self.model)
        if where_clauses is not None:
            stmt = stmt.where(sm.and_(*where_clauses))
        if limit is not None:
            stmt = stmt.limit(limit)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        entity = await self.session.exec(stmt)
        return entity.all()

    async def delete(self, instance: AbstractModel) -> NoReturn:
        await self.session.delete(instance)
        await self.session.flush()
        await self.session.commit()
