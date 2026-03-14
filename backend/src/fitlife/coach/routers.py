from uuid import UUID

from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from fitlife.auth.dependencies import CurrentUserDep
from fitlife.coach.dependencies import CoachServiceDep
from fitlife.config import settings
from fitlife.schemas import BadResponse, OkResponse, UserAddSchema, UserSchema
from fitlife.utils import custom_key_builder

router = APIRouter()

title = '🏋️ Coaches'


@router.post(
    '/coaches',
    summary='Add new coach',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    description='Add new coach to the database',
    responses={
        status.HTTP_201_CREATED: {
            'model': OkResponse,
            'description': 'Member successfully created.',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Coach with that phone or email already exists.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'Some error occurred while adding coach.',
        },
    },
)
async def add_coach(coach: UserAddSchema, service: CoachServiceDep, current_user: CurrentUserDep):
    return await service.create_user(coach)


@router.get(
    '/coaches',
    summary='Get all coaches',
    tags=[title],
    description='Get all coaches from the database.',
    response_model=list[UserSchema],
    responses={
        status.HTTP_200_OK: {
            'model': list[UserSchema],
            'description': 'Coaches successfully retrieved.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'An error occurred when you tried to retrieve a coaches.',
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
    description='Get specific coach from database',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Coach successfully retrieved.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Coach with that id does not exist.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'An error occurred when you tried to retrieve a coaches.',
        },
    },
)
async def get_specific_coach(coach_uuid: UUID, service: CoachServiceDep, current_user: CurrentUserDep):
    return await service.get_user(coach_uuid)


@router.put(
    '/coaches/{coach_uuid}',
    summary='Update specific coach',
    tags=[title],
    description='Update specific coach in the database',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Coach successfully updated.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Coach with that id does not exist.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'An error occurred when you tried to update a coaches.',
        },
    },
)
async def update_coach(coach_uuid: UUID, coach: UserAddSchema, service: CoachServiceDep, current_user: CurrentUserDep):
    return await service.update_user(coach_uuid, coach)


@router.delete(
    '/coaches/{coach_uuid}',
    summary='Delete specific coach',
    tags=[title],
    description='Delete specific coach in the database',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Coach successfully deleted.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Coach with that id does not exist.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'An error occurred when you tried to delete a coaches.',
        },
    },
)
async def delete_coach(coach_uuid: UUID, service: CoachServiceDep, current_user: CurrentUserDep):
    return await service.delete_user(coach_uuid)
