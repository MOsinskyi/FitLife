from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from fitlife.exceptions import UserAlreadyExists
from fitlife.schemas import UserRegisterSchema, UserSchema, UserUpdateSchema

from .dependencies import MemberServiceDep

member_router = APIRouter(prefix='/members', tags=['👨‍👩‍👧‍👦 Members'])


@member_router.get(
    '/{user_id}',
    response_model=UserSchema,
    description='Get member profile',
    responses={
        status.HTTP_200_OK: {
            'description': 'Success',
            'model': UserSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def get_member(user_id: UUID, service: MemberServiceDep):
    try:
        return await service.get_member_profile(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@member_router.get(
    '/',
    response_model=list[UserSchema],
    description='Get all members',
    responses={
        status.HTTP_200_OK: {
            'description': 'Success',
            'model': list[UserSchema],
        },
    },
)
async def get_members(service: MemberServiceDep):
    return await service.get_all_members()


@member_router.post(
    '/',
    response_model=UserSchema,
    description='Register new member',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Success',
            'model': UserSchema,
        },
        status.HTTP_409_CONFLICT: {
            'description': 'User already exists',
        },
    },
)
async def register_member(member_data: UserRegisterSchema, service: MemberServiceDep):
    try:
        return await service.register_member(member_data)
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@member_router.put(
    '/{user_id}',
    response_model=UserSchema,
    description='Update member profile',
    responses={
        status.HTTP_200_OK: {
            'description': 'Success',
            'model': UserSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Not found',
        },
    },
)
async def update_member(user_id: UUID, member_data: UserUpdateSchema, service: MemberServiceDep):
    try:
        return await service.update_member_profile(user_id, member_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@member_router.delete(
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
async def delete_member(user_id: UUID, service: MemberServiceDep):
    try:
        await service.delete_member_profile(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
