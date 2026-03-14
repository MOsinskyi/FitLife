from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.exc import NoResultFound

from fitlife.cache import clear_cache
from fitlife.logger import logger
from fitlife.repositories import UserRepository
from fitlife.schemas import OkResponse, UserAddSchema
from fitlife.security import SecurityDep

if TYPE_CHECKING:
    from fitlife.models import UserBase


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

    async def get_users(self) -> list['UserBase']:
        try:
            return await self.repository.get_all()
        except Exception as e:
            logger.error('Failed to get users %s', e)
            raise HTTPException(status_code=400, detail='Failed to get users') from e

    async def get_user(self, user_id: UUID) -> 'UserBase':
        try:
            return await self.repository.get_by_id(user_id)
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail='User not found') from e
        except Exception as e:
            logger.error('Failed to get user with uuid: %s, error: %s', user_id, e)
            raise HTTPException(status_code=400, detail='Failed to get user') from e

    async def update_user(self, user_id: UUID, data: UserAddSchema) -> OkResponse:

        user = await self.get_user(user_id)

        try:
            await self.repository.update(user, data)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='User updated successfully')
        except Exception as e:
            logger.error('Failed to update user with uuid: %s, error: %s', user_id, e)
            raise HTTPException(status_code=400, detail='Failed to update user') from e

    async def delete_user(self, user_id: UUID) -> OkResponse:

        user = await self.get_user(user_id)

        try:
            await self.repository.delete(user)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='User deleted successfully')
        except Exception as e:
            logger.error('Failed to delete user with uuid: %s, error: %s', user_id, e)
            raise HTTPException(status_code=400, detail='Failed to delete user') from e

    async def create_user(self, data: UserAddSchema, security: SecurityDep) -> OkResponse:

        if await self.repository.get_by_email(data.email):
            raise HTTPException(status_code=409, detail='User with this email already exists')

        if await self.repository.get_by_phone_number(data.phone_number):
            raise HTTPException(status_code=409, detail='User with this phone number already exists')

        await self.hash_password(data, security)

        try:
            await self.repository.create(data)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='User created successfully')
        except Exception as e:
            logger.error('Failed to create user, error: %s', e)
            raise HTTPException(status_code=400, detail='Failed to create user') from e

    @staticmethod
    async def hash_password(data: UserAddSchema, security: SecurityDep):
        try:
            dump_data = data.model_dump()
            for k, v in dump_data.items():
                if k == 'password':
                    setattr(data, k, security.hash_password(v))
                continue
        except Exception as e:
            logger.error('Failed to create user, error: %s', e)
            raise HTTPException(status_code=400, detail='Failed to hash password') from e
