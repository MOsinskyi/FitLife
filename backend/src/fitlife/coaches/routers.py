from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from fitlife.exceptions import UserAlreadyExists

from .dependencies import CoachServiceDep
from .schemas import CoachRegisterSchema, CoachSchema, CoachUpdateSchema

coach_router = APIRouter(prefix='/coaches', tags=['🏋️ Coaches'])


@coach_router.get(
    '/{user_id}',
    response_model=CoachSchema,
    description='Get member profile',
    responses={
        status.HTTP_200_OK: {
            'description': 'Success',
            'model': CoachSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def get_coach(user_id: UUID, service: CoachServiceDep):
    try:
        return await service.get_coach_profile(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@coach_router.get(
    '/',
    response_model=list[CoachSchema],
    description='Get all members',
    responses={
        status.HTTP_200_OK: {
            'description': 'Success',
            'model': list[CoachSchema],
        },
    },
)
async def get_coaches(service: CoachServiceDep):
    return await service.get_all_coaches()


@coach_router.post(
    '/',
    response_model=CoachSchema,
    description='Register new member',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Success',
            'model': CoachSchema,
        },
        status.HTTP_409_CONFLICT: {
            'description': 'User already exists',
        },
    },
)
async def register_coach(member_data: CoachRegisterSchema, service: CoachServiceDep):
    try:
        return await service.register_coach(member_data)
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@coach_router.put(
    '/{user_id}',
    response_model=CoachSchema,
    description='Update member profile',
    responses={
        status.HTTP_200_OK: {
            'description': 'Success',
            'model': CoachSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def update_coach(user_id: UUID, member_data: CoachUpdateSchema, service: CoachServiceDep):
    try:
        return await service.update_coach_profile(user_id, member_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@coach_router.delete(
    '/{user_id}',
    description='Delete member profile',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'Success',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def delete_coach(user_id: UUID, service: CoachServiceDep):
    try:
        await service.delete_coach(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
