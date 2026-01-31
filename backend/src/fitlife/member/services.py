from uuid import UUID

from fitlife.logger import logger
from fitlife.member.repositories import MemberRepository
from fitlife.member.schemas import MemberAddSchema
from fitlife.models import Base
from fitlife.schemas import BadResponse, OkResponse

Response = OkResponse | BadResponse


class MemberService:
    def __init__(self, repository: MemberRepository):
        self.repository = repository

    async def member_with_phone_number_exists(self, member: MemberAddSchema) -> bool:
        """
        Асинхронна функція, яка повертає статус - чи існує даний користувач з таким номером телефону?
        :param member: Користувач.
        :return: Статус існує чи ні.
        """
        exiting_member = await self.repository.get_member_by_phone_number(member.phone)
        result = exiting_member is not None
        logger.debug('Result: %s', result)
        return result

    async def get_members(self) -> list[Base] | None:
        """
        Асинхронна функція, яка повертає всіх користувачів.
        :return: Список користувачів.
        """
        result = None

        try:
            result = await self.repository.get_all()
            logger.info('Result: %s', result)
        except Exception as e:
            logger.error('Exception: %s', e)

        return result

    async def get_member(self, member_uuid: UUID) -> Base | None:
        """
        Асинхронна функція, яка повертає користувача за його UUID.
        :param member_uuid: UUID користувача.
        :return: Користувача, якщо такий існує інакше None
        """
        result = None

        try:
            result = await self.repository.get_by_id(member_uuid)
            logger.info('Result: %s', result)
        except Exception as e:
            logger.error('Exception: %s', e)

        return result

    async def update_member(self, member_uuid: UUID, data: MemberAddSchema) -> Response:
        """
        Асинхронна функція яка оновлює користувача за його UUID.
        :param member_uuid: UUID користувача.
        :param data: Нові дані.
        """
        try:
            await self.repository.update(member_uuid, data)
            return OkResponse(msg='Member successfully updated.')
        except Exception as e:
            logger.error('Помилка при оновленні користувача: %s', e)
            return BadResponse(msg="Member doesn't updated")

    async def delete_member(self, member_uuid: UUID) -> Response:
        """
        Асинхронна функція, яка видаляє користувача за його UUID.
        :param member_uuid: UUID користувача.
        """
        try:
            await self.repository.delete(member_uuid)
            return OkResponse(msg='Member successfully deleted.')
        except Exception as e:
            logger.error('Помилка при видаленні користувача: %s', e)
            return BadResponse(msg="Member doesn't deleted")

    async def create_member(self, member: MemberAddSchema) -> Response:
        """
        Асинхронна функція, яка створює користувача.
        :param member: Користувач з даними.
        :return: Відповідь сервера.
        """
        is_member_exists = await self.member_with_phone_number_exists(member)

        if is_member_exists:
            logger.info('Member already exists: %s', member)
            return BadResponse(msg='Member already exists')

        await self.repository.create(member)
        logger.info('Member created')
        return OkResponse(msg='Member successfully created')
