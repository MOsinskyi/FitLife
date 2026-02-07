from uuid import UUID

from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from fitlife.schemas import BadResponse, OkResponse

from ..config import settings
from ..utils import custom_key_builder
from .dependencies import TrainingSessionServiceDep
from .schemas import TrainingSessionAddSchema, TrainingSessionSchema

router = APIRouter()

title = '📅 Training Sessions'


@router.post(
    '/training_sessions',
    summary='Add new training session.',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    description='Add new training session to the database.',
    responses={
        status.HTTP_201_CREATED: {
            'model': OkResponse,
            'description': 'Training session successfully created.',
        },
        status.HTTP_409_CONFLICT: {'model': BadResponse, 'description': 'Training with title already exists.'},
    },
)
async def add_training_session(training_session: TrainingSessionAddSchema, service: TrainingSessionServiceDep):
    return await service.create_training_session(training_session)


@router.get(
    '/training_sessions',
    summary='Get all training sessions.',
    tags=[title],
    description='Get all training session from the database.',
    response_model=list[TrainingSessionSchema],
)
@cache(
    expire=60,
    namespace=settings.cache.namespace.training_session,
    key_builder=custom_key_builder,
)
async def get_training_sessions(service: TrainingSessionServiceDep):
    return await service.get_training_sessions()


@router.delete(
    '/training_sessions/{training_session_uuid}',
    summary='Delete training session',
    tags=[title],
    description='Delete specific training session from database.',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Member successfully deleted',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Member not found',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'Failed to delete member',
        },
    },
)
async def delete_training_session(training_session_uuid: UUID, service: TrainingSessionServiceDep):
    return await service.delete_training_session(training_session_uuid)
