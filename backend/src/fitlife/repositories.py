from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserUpdateSchema


class BaseUserRepository[T](ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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
