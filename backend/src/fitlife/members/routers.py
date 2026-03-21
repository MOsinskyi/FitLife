from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from fitlife.schemas import UserSchema

from .dependencies import MemberServiceDep

router = APIRouter(prefix='/members', tags=['👨‍👩‍👧‍👦 Members'])


@router.get(
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


@router.get(
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


async def register_member(service: MemberServiceDep):
    pass
