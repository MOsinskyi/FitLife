import uuid
from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.models import Base


class BaseRepository(ABC):
    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID):
        pass

    @abstractmethod
    async def create(self, data: BaseModel):
        pass

    @abstractmethod
    async def update(self, id_: uuid.UUID, data: BaseModel):
        pass

    @abstractmethod
    async def delete(self, id_: uuid.UUID):
        pass


class BaseSqlAlchemyRepository(BaseRepository):
    def __init__(self, model: type[Base], session: AsyncSession):
        self.session = session
        self.model = model

    async def get_all(self):
        query = select(self.model)
        response = await self.session.execute(query)
        return response.scalars().all()

    async def get_by_id(self, id_: uuid.UUID):
        query = select(self.model).where(self.model.id == id_)
        response = await self.session.execute(query)
        return response.scalars().first()

    async def create(self, data: BaseModel):
        new_model = self.model(**data.model_dump())
        self.session.add(new_model)
        await self.session.commit()

    async def update(self, id_: uuid.UUID, data: BaseModel):
        existing_model = await self.get_by_id(id_)
        await self.session.merge(existing_model)
        await self.session.commit()

    async def delete(self, id_: uuid.UUID):
        existing_model = await self.get_by_id(id_)
        await self.session.delete(existing_model)
        await self.session.commit()
