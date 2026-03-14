import uuid
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fitlife.models import Base, UserBase

T = TypeVar('T')


class BaseRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[T]:
        pass

    @abstractmethod
    async def get_by_id(self, id_: uuid.UUID) -> T:
        pass

    @abstractmethod
    async def create(self, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def update(self, existing_model: Base, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def delete(self, existing_model: Base) -> None:
        pass


class UserRepository(BaseRepository):
    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> T:
        pass

    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> T:
        pass


class BaseSqlAlchemyRepository(BaseRepository):
    def __init__(self, model: type[T], session: AsyncSession):
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

    async def update(self, existing_model: Base, data: BaseModel):
        new_values = data.model_dump()

        for k, v in new_values.items():
            setattr(existing_model, k, v)

        await self.session.commit()
        await self.session.refresh(existing_model)

    async def delete(self, existing_model: Base):
        await self.session.delete(existing_model)
        await self.session.commit()


class UserSqlAlchemyRepository(UserRepository, BaseSqlAlchemyRepository):
    def __init__(self, model: type[UserBase], session: AsyncSession):
        super().__init__(model, session)
        self.model = model

    async def get_by_phone_number(self, phone_number: str) -> T:
        query = select(self.model).where(self.model.phone_number == phone_number)
        response = await self.session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr) -> T:
        query = select(self.model).where(self.model.email == email)
        response = await self.session.execute(query)
        return response.scalars().first()
