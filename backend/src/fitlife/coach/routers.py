from uuid import UUID

from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from fitlife.auth.dependencies import CurrentCoachDep, CurrentUserDep
from fitlife.coach.dependencies import CoachServiceDep
from fitlife.config import settings
from fitlife.schemas import BadResponse, OkResponse, UserCredentialsSchema, UserRegisterSchema
from fitlife.utils import custom_key_builder

router = APIRouter()

title = '🏋️ Coaches'


@router.get(
    '/coaches',
    summary='Get all coaches',
    tags=[title],
    description='Get all coaches from the database. Any authenticated user.',
    response_model=list[UserCredentialsSchema],
    responses={
        status.HTTP_200_OK: {
            'model': list[UserCredentialsSchema],
            'description': 'Coaches successfully retrieved.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'An error occurred when you tried to retrieve coaches.',
        },
    },
)
@cache(
    expire=60,
    namespace=settings.cache.namespace.coach,
    key_builder=custom_key_builder,
)
async def get_coaches(service: CoachServiceDep, current_user: CurrentUserDep):
    return await service.get_users()


@router.get(
    '/coaches/{coach_uuid}',
    summary='Get specific coach by id',
    tags=[title],
    description='Get specific coach from database. Any authenticated user.',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Coach successfully retrieved.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Coach with that id does not exist.',
        },
    },
)
async def get_specific_coach(coach_uuid: UUID, service: CoachServiceDep, current_user: CurrentUserDep):
    return await service.get_user(coach_uuid)


@router.put(
    '/coaches/{coach_uuid}',
    summary='Update specific coach',
    tags=[title],
    description='Update specific coach in the database. Coach only.',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Coach successfully updated.',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': BadResponse,
            'description': 'Coaches only.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Coach with that id does not exist.',
        },
    },
)
async def update_coach(
    coach_uuid: UUID,
    coach: UserRegisterSchema,
    service: CoachServiceDep,
    current_user: CurrentCoachDep,  # coach only
):
    return await service.update_user(coach_uuid, coach)


@router.delete(
    '/coaches/{coach_uuid}',
    summary='Delete specific coach',
    tags=[title],
    description='Delete specific coach in the database. Coach only.',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Coach successfully deleted.',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': BadResponse,
            'description': 'Coaches only.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Coach with that id does not exist.',
        },
    },
)
async def delete_coach(coach_uuid: UUID, service: CoachServiceDep, current_user: CurrentCoachDep):  # coach only
    return await service.delete_user(coach_uuid)
