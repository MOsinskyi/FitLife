import uuid
from abc import ABC, abstractmethod

from logger import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.models import Base


class BaseRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Base]:
        """
        Отримати усі сутності
        """
        pass

    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID) -> Base:
        pass

    @abstractmethod
    async def create(self, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def update(self, id_: uuid.UUID, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def delete(self, id_: uuid.UUID) -> None:
        pass


class BaseSqlAlchemyRepository(BaseRepository):
    def __init__(self, model: type[Base], session: AsyncSession):
        self.session = session
        self.model = model
        logger.info(
            '%s initialized with params %s and %s', self.__class__.__name__, model.__repr__, self.session.__repr__
        )

    async def get_all(self):
        query = select(self.model)
        response = await self.session.execute(query)
        logger.info('%s get all %s', self.__class__.__name__, response)
        return response.scalars().all()

    async def get_by_id(self, id_: uuid.UUID):
        query = select(self.model).where(self.model.id == id_)
        response = await self.session.execute(query)
        logger.info('%s get by id %s', self.__class__.__name__, response)
        return response.scalars().first()

    async def create(self, data: BaseModel):
        new_model = self.model(**data.model_dump())
        self.session.add(new_model)
        await self.session.commit()
        logger.info('%s create %s', self.__class__.__name__, new_model)

    async def update(self, id_: uuid.UUID, data: BaseModel):
        existing_model = await self.get_by_id(id_)
        await self.session.merge(existing_model)
        await self.session.commit()
        logger.info('%s update %s', self.__class__.__name__, existing_model)

    async def delete(self, id_: uuid.UUID):
        existing_model = await self.get_by_id(id_)
        await self.session.delete(existing_model)
        await self.session.commit()
        logger.info('%s delete %s', self.__class__.__name__, existing_model)
