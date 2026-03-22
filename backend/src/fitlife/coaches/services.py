from typing import TYPE_CHECKING
from uuid import UUID

from fitlife.exceptions import UserAlreadyExists

from ..schemas import UserRoles
from .models import CoachModel

if TYPE_CHECKING:
    from fitlife.security import Security

    from .repositories import CoachRepository
    from .schemas import CoachRegisterSchema, CoachUpdateSchema


class CoachService:
    def __init__(self, repository: 'CoachRepository', security: 'Security'):
        self.repository = repository
        self.security = security

    async def get_coach_profile(self, member_id: UUID) -> CoachModel:
        user = await self.repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Coach not found')
        return user

    async def register_coach(self, user_data: 'CoachRegisterSchema') -> CoachModel:
        new_user = CoachModel(**user_data.model_dump())

        if await self.repository.get_user_by_phone(new_user.phone_number):
            raise UserAlreadyExists('User with this phone number already exists')

        if await self.repository.get_user_by_email(new_user.email):
            raise UserAlreadyExists('User with this email already exists')

        user = await self.repository.create_user(new_user)

        user.role = UserRoles.COACH.value
        user.password = self.security.hash_password(user_data.password)

        return user

    async def update_coach_profile(self, member_id: UUID, user_data: 'CoachUpdateSchema') -> CoachModel:
        user = await self.repository.update_user(member_id, user_data)
        if not user:
            raise ValueError('Coach not found')
        return user

    async def delete_coach(self, member_id: UUID) -> None:
        user = await self.repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Coach not found')

        await self.repository.delete_user(member_id)

    async def get_all_coaches(self) -> list[CoachModel]:
        return await self.repository.get_users()
