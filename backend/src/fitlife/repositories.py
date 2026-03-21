from abc import ABC, abstractmethod
from uuid import UUID


class BaseUserRepository[T](ABC):
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
    async def update_user(self, user_id: UUID, data: T) -> T | None:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        pass
