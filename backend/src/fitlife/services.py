import functools
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException

from fitlife.cache import clear_cache
from fitlife.logger import logger
from fitlife.repositories import UserRepository
from fitlife.schemas import OkResponse, UserAddSchema
from fitlife.security import SecurityDep

if TYPE_CHECKING:
    from fitlife.models import UserBase


def servicemethod(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error('An unknown error has occurred: %s', e)
            raise HTTPException(status_code=500, detail='An unknown error has occurred') from e

    return wrapper


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        background_tasks: BackgroundTasks,
        security: SecurityDep,
        cache_namespace: str = '',
    ):
        self.background_tasks = background_tasks
        self.repository = repository
        self.namespace = cache_namespace
        self.security = security

    @servicemethod
    async def get_users(self) -> list['UserBase']:
        return await self.repository.get_all()

    @servicemethod
    async def get_user(self, user_id: UUID) -> 'UserBase':
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        return user

    @servicemethod
    async def update_user(self, user_id: UUID, data: UserAddSchema) -> OkResponse:
        user = await self.get_user(user_id)
        await self.repository.update(user, data)
        await clear_cache(self.background_tasks, self.namespace)

        return OkResponse(msg='User updated successfully')

    @servicemethod
    async def delete_user(self, user_id: UUID) -> OkResponse:

        user = await self.get_user(user_id)

        await self.repository.delete(user)
        await clear_cache(self.background_tasks, self.namespace)
        return OkResponse(msg='User deleted successfully')

    @servicemethod
    async def create_user(self, data: UserAddSchema, security: SecurityDep) -> OkResponse:

        if await self.repository.get_by_email(data.email):
            raise HTTPException(status_code=409, detail='User with this email already exists')

        if await self.repository.get_by_phone_number(data.phone_number):
            raise HTTPException(status_code=409, detail='User with this phone number already exists')

        await self.hash_password(data, security)

        await self.repository.create(data)
        await clear_cache(self.background_tasks, self.namespace)
        return OkResponse(msg='User created successfully')

    @servicemethod
    async def get_user_by_phone_number(self, phone_number: str):
        return await self.repository.get_by_phone_number(phone_number)

    @staticmethod
    async def hash_password(data: UserAddSchema, security: SecurityDep):
        dump_data = data.model_dump()
        for k, v in dump_data.items():
            if k == 'password':
                setattr(data, k, security.hash_password(v))
            continue
