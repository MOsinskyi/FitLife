from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException, Response, status
from fastapi.responses import JSONResponse

from fitlife.logger import logger

from ..cache import clear_cache
from ..services import servicemethod
from .repositories import TrainingSessionRepository

if TYPE_CHECKING:
    from .models import TrainingSessionModel
    from .schemas import TrainingSessionAddSchema


class TrainingSessionService:
    def __init__(
        self,
        repository: TrainingSessionRepository,
        background_tasks: BackgroundTasks,
        cache_namespace: str = '',
    ) -> None:
        self.repository = repository
        self.namespace = cache_namespace
        self.background_tasks = background_tasks

    async def get_training_sessions(self) -> list['TrainingSessionModel']:
        try:
            return await self.repository.get_all()
        except Exception as e:
            logger.error('An unknown error has occurred: %s', e, exc_info=True)
            raise HTTPException(status_code=400, detail='Failed to get training sessions.') from e

    @servicemethod
    async def get_training_session(self, id_: UUID) -> 'TrainingSessionModel':
        obj = await self.repository.get_by_id(id_)

        if not obj:
            logger.error('Сесії не знайдено')
            raise HTTPException(status_code=404, detail='Training session not found.') from None

        return obj

    async def update_training_session(self, id_: UUID, data: 'TrainingSessionAddSchema') -> Response:

        training_session = await self.get_training_session(id_)

        if not training_session:
            raise HTTPException(status_code=404, detail='Training session not found.')

        try:
            await self.repository.update(training_session.id, data)
            await clear_cache(self.background_tasks, self.namespace)
            return JSONResponse(
                content={
                    'success': True,
                    'msg': 'Training session updated successfully.',
                }
            )
        except Exception as e:
            logger.error('An unknown error has occurred: %s', e)
            raise HTTPException(status_code=400, detail='Failed to update training session.') from e

    async def delete_training_session(self, id_: UUID) -> Response:

        training_session = await self.get_training_session(id_)

        try:
            await self.repository.delete(training_session)
            await clear_cache(self.background_tasks, self.namespace)
            return JSONResponse(
                content={
                    'success': True,
                    'msg': 'User deleted successfully.',
                }
            )
        except Exception as e:
            logger.error('An unknown error has occurred: %s.', e)
            raise HTTPException(status_code=400, detail='Failed to delete training session.') from e

    async def create_training_session(self, data: 'TrainingSessionAddSchema') -> Response:

        if await self.repository.get_by_title(data.title):
            raise HTTPException(status_code=409, detail='Training session with this title already exists.') from None

        try:
            await self.repository.create(data)
            await clear_cache(self.background_tasks, self.namespace)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    'success': True,
                    'msg': 'Training session created successfully.',
                },
            )
        except Exception as e:
            logger.error('An unknown error has occurred: %s.', e)
            raise HTTPException(status_code=400, detail='Failed to create training session.') from e

    async def book_training_session(self, training_session_uuid: UUID, member_uuid: UUID):

        if not await self.repository.get_by_id(training_session_uuid):
            raise HTTPException(status_code=404, detail='Training session not found.')

        if await self.repository.is_member_in_training_session(training_session_uuid, member_uuid):
            raise HTTPException(status_code=409, detail='Member already booked this training session.')

        training_session = await self.repository.add_member_to_training_session(training_session_uuid, member_uuid)
        await clear_cache(self.background_tasks, self.namespace)

        return training_session
