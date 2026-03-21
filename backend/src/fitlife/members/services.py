from typing import TYPE_CHECKING
from uuid import UUID

from .models import MemberModel

if TYPE_CHECKING:
    from ..schemas import UserRegisterSchema, UserUpdateSchema
    from .repositories import MemberRepository


class MemberService:
    def __init__(self, repository: 'MemberRepository'):
        self.repository = repository

    async def get_member_profile(self, member_id: UUID) -> MemberModel:
        user = await self.repository.get_user_by_id(member_id)
        if not user:
            raise ValueError('Member not found')
        return user

    async def register_member(self, user_data: 'UserRegisterSchema') -> MemberModel:
        new_user = MemberModel(**user_data.model_dump())

        user = await self.repository.create_user(new_user)

        user.role = 'member'

        return user

    async def update_member_profile(self, member_id: UUID, user_data: 'UserUpdateSchema') -> MemberModel:
        user = await self.repository.update_user(member_id, user_data)
        if not user:
            raise ValueError('Member not found')
        return user

    async def delete_member_profile(self, member_id: UUID) -> None:
        await self.repository.delete_user(member_id)
