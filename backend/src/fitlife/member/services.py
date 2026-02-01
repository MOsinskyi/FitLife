from uuid import UUID

from fastapi import BackgroundTasks, HTTPException

from fitlife.cache import clear_cache
from fitlife.config import settings
from fitlife.logger import logger
from fitlife.member.repositories import MemberRepository
from fitlife.models import Base
from fitlife.schemas import OkResponse, Response, UserAddSchema


class MemberService:
    def __init__(self, repository: MemberRepository, background_tasks: BackgroundTasks):
        self.repository = repository
        self.background_tasks = background_tasks
        self.namespace = settings.cache.namespace.member

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
        await self.is_member_exists(member_uuid)

        try:
            return await self.repository.get_by_id(member_uuid)
        except Exception as e:
            logger.error('Exception: %s', e)

    async def update_member(self, member_uuid: UUID, data: UserAddSchema) -> Base:
        """
        Асинхронна функція яка оновлює користувача за його UUID.
        :param member_uuid: UUID користувача.
        :param data: Нові дані.
        """
        await self.is_member_exists(member_uuid)

        try:
            await self.repository.update(member_uuid, data)
            await clear_cache(self.background_tasks, self.namespace)
            return await self.get_member(member_uuid)
        except Exception as e:
            logger.error('Помилка при оновленні користувача: %s', e)
            raise HTTPException(status_code=400, detail="Member doesn't updated") from None

    async def delete_member(self, member_uuid: UUID) -> Response:
        """
        Асинхронна функція, яка видаляє користувача за його UUID.
        :param member_uuid: UUID користувача.
        """
        await self.is_member_exists(member_uuid)

        try:
            await self.repository.delete(member_uuid)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='Member successfully deleted.')
        except Exception as e:
            logger.error('Помилка при видаленні користувача: %s', e)
            raise HTTPException(status_code=400, detail="Member doesn't deleted") from None

    async def is_member_exists(self, member_uuid: UUID):
        if not await self.repository.get_by_id(member_uuid):
            raise HTTPException(status_code=404, detail="Member doesn't exist") from None

    async def create_member(self, member: UserAddSchema) -> Response:
        """
        Асинхронна функція, яка створює користувача.
        :param member: Користувач з даними.
        :return: Відповідь сервера.
        """
        if await self.repository.get_by_phone_number(member.phone_number):
            raise HTTPException(status_code=409, detail='Member with that phone number already exists.') from None

        if await self.repository.get_by_email(member.email):
            raise HTTPException(status_code=409, detail='Member with that email already exists.') from None

        await self.repository.create(member)
        await clear_cache(self.background_tasks, self.namespace)
        logger.info('Member created')
        return OkResponse(msg='Member successfully created')
