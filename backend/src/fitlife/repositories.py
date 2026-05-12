from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserBase
from .schemas import UserUpdateSchema


class IUserRepository[T](ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> T | None:
        pass

    @abstractmethod
    async def create_user(self, user: T) -> T | None:
        pass

    @abstractmethod
    async def get_users(self) -> list[T]:
        pass

    @abstractmethod
    async def update_user(self, user_id: UUID, data: UserUpdateSchema) -> T | None:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> T | None:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> T | None:
        pass


class BaseUserRepository[T](IUserRepository):
    model = UserBase
    update_model_schema = UserUpdateSchema

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> T | None:
        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: T) -> T | None:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_users(self) -> list[T]:
        smtp = select(self.model)
        result = await self.session.execute(smtp)
        return list(result.scalars().all())

    async def update_user(self, user_id: UUID, data: update_model_schema) -> T | None:
        smtp = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(
                **data.model_dump(
                    exclude_unset=True, exclude_none=True, exclude_defaults=True
                )
            )
            .returning(self.model)
        )
        result = await self.session.execute(smtp)
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: UUID) -> None:
        stmt = delete(self.model).where(self.model.id == user_id)
        await self.session.execute(stmt)

    async def get_user_by_phone(self, phone: str) -> T | None:
        stmt = select(self.model).where(self.model.phone_number == phone)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> T | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
