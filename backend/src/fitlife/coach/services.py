from uuid import UUID

from fastapi import BackgroundTasks

from fitlife.cache import clear_cache
from fitlife.coach.models import CoachModel
from fitlife.coach.repositories import CoachRepository
from fitlife.config import settings
from fitlife.logger import logger
from fitlife.schemas import BadResponse, OkResponse, Response, UserAddSchema


class CoachService:
    def __init__(self, repository: CoachRepository, background_tasks: BackgroundTasks):
        self.repository = repository
        self.background_tasks = background_tasks
        self.namespace = settings.cache.namespace.coach

    async def get_coaches(self) -> list[CoachModel] | None:
        try:
            return await self.repository.get_all()
        except Exception as e:
            logger.error('Failed to get all coaches %s', e)
            return None

    async def get_coach(self, coach_id: UUID) -> CoachModel | None:
        try:
            return await self.repository.get_by_id(coach_id)
        except Exception as e:
            logger.error('Failed to get coach with uuid: %s error: %s', coach_id, e)
            return None

    async def update_coach(self, coach_id: UUID, data: UserAddSchema) -> Response:
        try:
            await self.repository.update(coach_id, data)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='Coach successfully updated')
        except Exception as e:
            logger.error('Failed to update coach with uuid: %s error: %s', coach_id, e)
            return BadResponse(msg='Failed to update coach')

    async def delete_coach(self, coach_id: UUID) -> Response:
        try:
            await self.repository.delete(coach_id)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='Coach successfully deleted')
        except Exception as e:
            logger.error('Failed to delete coach with uuid: %s error: %s', coach_id, e)
            return BadResponse(msg='Failed to delete coach')

    async def create_coach(self, coach: UserAddSchema) -> Response:

        if self.repository.get_by_phone_number(coach.phone_number):
            return BadResponse(msg='Phone number already exists')

        if self.repository.get_by_email(coach.email):
            return BadResponse(msg='Email already exists')

        try:
            await self.repository.create(coach)
            await clear_cache(self.background_tasks, self.namespace)
            return OkResponse(msg='Coach successfully created')
        except Exception as e:
            logger.error('Failed to create coach with uuid: %s error: %s', coach.id, e)
            return BadResponse(msg='Failed to create coach')
