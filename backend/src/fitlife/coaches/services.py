from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import BackgroundTasks

from fitlife.cache import clear_cache
from fitlife.exceptions import UserAlreadyExists

from ..schemas import UserRoles
from .models import CoachModel

if TYPE_CHECKING:
    from fitlife.security import Security

    from .repositories import CoachRepository
    from .schemas import CoachRegisterSchema, CoachUpdateSchema


class CoachService:
    def __init__(
        self,
        repository: 'CoachRepository',
        security: 'Security',
        background_tasks: BackgroundTasks,
        cache_namespace: str,
    ):
        self._repository = repository
        self._security = security
        self._background_tasks = background_tasks
        self._cache_namespace = cache_namespace

    async def get_coach_profile(self, member_id: UUID) -> CoachModel:
        user = await self._repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Coach not found')
        return user

    async def register_coach(self, user_data: 'CoachRegisterSchema') -> CoachModel:
        new_user = CoachModel(**user_data.model_dump())

        if await self._repository.get_user_by_phone(new_user.phone_number):
            raise UserAlreadyExists('User with this phone number already exists')

        if await self._repository.get_user_by_email(new_user.email):
            raise UserAlreadyExists('User with this email already exists')

        user = await self._repository.create_user(new_user)

        user.role = UserRoles.COACH.value
        user.password = self._security.hash_password(user_data.password)

        await clear_cache(self._background_tasks, self._cache_namespace)

        return user

    async def update_coach_profile(self, member_id: UUID, user_data: 'CoachUpdateSchema') -> CoachModel:
        user = await self._repository.update_user(member_id, user_data)

        await clear_cache(self._background_tasks, self._cache_namespace)

        if not user:
            raise ValueError('Coach not found')
        return user

    async def delete_coach(self, member_id: UUID) -> None:
        user = await self._repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Coach not found')

        await self._repository.delete_user(member_id)

    async def get_all_coaches(self) -> list[CoachModel]:
        return await self._repository.get_users()
