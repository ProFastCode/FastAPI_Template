import abc
import uuid
from typing import Generic, TypeVar, Type

from sqlmodel.ext.asyncio.session import AsyncSession

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel], metaclass=abc.ABCMeta):
    def __init__(self, type_model: Type[AbstractModel], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def create(self, model: AbstractModel) -> AbstractModel:
        self.type_model.model_validate(model)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def read(self, ident: uuid.UUID) -> AbstractModel | None:
        entry = await self.session.get(self.type_model, ident)
        return entry
