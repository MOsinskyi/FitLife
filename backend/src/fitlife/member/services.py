from uuid import UUID

from fitlife.logger import logger
from fitlife.member.repositories import MemberRepository
from fitlife.member.schemas import MemberAddSchema
from fitlife.schemas import BadResponse, OkResponse


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    async def member_with_phone_number_exists(self, member: MemberAddSchema) -> bool:
        exiting_member = await self.repository.get_member_by_phone_number(member.phone)
        result = exiting_member is not None
        logger.debug('Result: %s', result)
        return result

    async def get_members(self):
        result = None

        try:
            result = await self.repository.get_all()
            logger.info('Result: %s', result)
        except Exception as e:
            logger.error('Exception: %s', e)

        return result

    async def get_member(self, member_uuid: UUID):
        result = None

        try:
            result = await self.repository.get_by_id(member_uuid)
            logger.info('Result: %s', result)
        except Exception as e:
            logger.error('Exception: %s', e)

        return result

    async def update_member(self, member_uuid: UUID, data: MemberAddSchema):
        return await self.repository.update(member_uuid, data)

    async def delete_member(self, member_uuid: UUID):
        return await self.repository.delete(member_uuid)

    async def create_member(self, member: MemberAddSchema) -> OkResponse | BadResponse:
        is_member_exists = await self.member_with_phone_number_exists(member)

        if is_member_exists:
            logger.info('Member already exists: %s', member)
            return BadResponse(msg='Member already exists')

        await self.repository.create(member)
        logger.info('Member created')
        return OkResponse(msg='Member successfully created')
