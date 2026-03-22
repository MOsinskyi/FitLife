from typing import TYPE_CHECKING
from uuid import UUID

from fitlife.exceptions import UserAlreadyExists

from .models import MemberModel

if TYPE_CHECKING:
    from fitlife.schemas import UserRegisterSchema, UserRoles, UserUpdateSchema
    from fitlife.security import Security

    from .repositories import MemberRepository


class MemberService:
    def __init__(self, repository: 'MemberRepository', security: 'Security'):
        self.repository = repository
        self.security = security

    async def get_member_profile(self, member_id: UUID) -> MemberModel:
        user = await self.repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Member not found')
        return user

    async def register_member(self, user_data: 'UserRegisterSchema') -> MemberModel:
        new_user = MemberModel(**user_data.model_dump())

        if await self.repository.get_user_by_phone(new_user.phone_number):
            raise UserAlreadyExists('User with this phone number already exists')

        if await self.repository.get_user_by_email(new_user.email):
            raise UserAlreadyExists('User with this email already exists')

        user = await self.repository.create_user(new_user)

        user.role = UserRoles.MEMBER.value
        user.password = self.security.hash_password(user_data.password)

        return user

    async def update_member_profile(self, member_id: UUID, user_data: 'UserUpdateSchema') -> MemberModel:
        user = await self.repository.update_user(member_id, user_data)
        if not user:
            raise ValueError('Member not found')
        return user

    async def delete_member_profile(self, member_id: UUID) -> None:
        user = await self.repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Member not found')

        await self.repository.delete_user(member_id)

    async def get_all_members(self) -> list[MemberModel]:
        return await self.repository.get_users()
