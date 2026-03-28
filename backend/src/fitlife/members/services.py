from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import BackgroundTasks

from fitlife.exceptions import UserAlreadyExists
from fitlife.schemas import UserRoles

from ..cache import clear_cache
from .models import MemberModel

if TYPE_CHECKING:
    from fitlife.schemas import UserRegisterSchema, UserUpdateSchema
    from fitlife.security import Security

    from .repositories import MemberRepository


class MemberService:
    def __init__(
        self,
        repository: 'MemberRepository',
        security: 'Security',
        background_tasks: BackgroundTasks,
        cache_namespace: str,
    ):
        self._repository = repository
        self._security = security
        self._background_tasks = background_tasks
        self._cache_namespace = cache_namespace

    async def get_member_profile(self, member_id: UUID) -> MemberModel:
        user = await self._repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Member not found')
        return user

    async def register_member(self, user_data: 'UserRegisterSchema') -> MemberModel:
        new_user = MemberModel(**user_data.model_dump())

        if await self._repository.get_user_by_phone(new_user.phone_number):
            raise UserAlreadyExists('User with this phone number already exists')

        if await self._repository.get_user_by_email(new_user.email):
            raise UserAlreadyExists('User with this email already exists')

        user = await self._repository.create_user(new_user)

        user.role = UserRoles.MEMBER.value
        user.password = self._security.hash_password(user_data.password)

        await clear_cache(self._background_tasks, self._cache_namespace)

        return user

    async def update_member_profile(self, member_id: UUID, user_data: 'UserUpdateSchema') -> MemberModel:
        user = await self._repository.update_user(member_id, user_data)

        await clear_cache(self._background_tasks, self._cache_namespace)

        if not user:
            raise ValueError('Member not found')
        return user

    async def delete_member_profile(self, member_id: UUID) -> None:
        user = await self._repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Member not found')

        await self._repository.delete_user(member_id)

    async def get_all_members(self) -> list[MemberModel]:
        return await self._repository.get_users()
