import abc

import sqlmodel as sm
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import (Generic, List, NoReturn, Optional, Sequence,
                               Type, TypeVar)

AbstractModel = TypeVar('AbstractModel', bound=sm.SQLModel)


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
        where_clauses: Optional[List[sm.DefaultClause] | List[bool]] = None,
    ) -> Optional[AbstractModel]:
        if ident is not None:
            return await self.session.get(self.model, ident)
        stmt = sm.select(self.model).where(sm.and_(*where_clauses))
        entity = await self.session.exec(stmt)
        return entity.first()

    async def retrieve_many(
        self,
        where_clauses: Optional[List[sm.DefaultClause] | List[bool]] = None,
    ) -> Optional[Sequence[AbstractModel]]:
        stmt = sm.select(self.model).where(sm.and_(*where_clauses))
        entity = await self.session.exec(stmt)
        return entity.all()

    async def update(self, ident: int, **values) -> NoReturn:
        stmt = (
            sm.update(self.model).where(self.model.id == ident).values(values)
        )
        await self.session.execute(stmt)

    async def delete(self, instance: AbstractModel) -> NoReturn:
        await self.session.delete(instance)
        await self.session.flush()
