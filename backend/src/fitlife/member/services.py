from uuid import UUID

from fastapi import HTTPException, status

from fitlife.member.repositories import MemberRepository
from fitlife.member.schemas import MemberAddSchema


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    async def member_with_phone_number_exists(self, member: MemberAddSchema) -> bool:
        exiting_member = await self.repository.get_member_by_phone_number(member.phone)
        return exiting_member is not None

    async def get_members(self):
        return await self.repository.get_all()

    async def get_member(self, member_uuid: UUID):
        return await self.repository.get_by_id(member_uuid)

    async def update_member(self, member_uuid: UUID, data: MemberAddSchema):
        return await self.repository.update(member_uuid, data)

    async def delete_member(self, member_uuid: UUID):
        return await self.repository.delete(member_uuid)

    async def create_member(self, member: MemberAddSchema) -> None:
        if await self.member_with_phone_number_exists(member):
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Member already exists')
            return None

        return await self.repository.create(member)
