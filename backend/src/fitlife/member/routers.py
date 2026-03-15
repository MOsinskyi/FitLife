from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette import status

from fitlife.auth.dependencies import CurrentCoachDep
from fitlife.config import settings
from fitlife.member.dependencies import MemberServiceDep
from fitlife.schemas import BadResponse, OkResponse, UserRegisterSchema, UserSchema
from fitlife.utils import custom_key_builder

router = APIRouter()

title = '👨‍👩‍ Members'


@router.get(
    '/members',
    summary='Get all members',
    tags=[title],
    description='Get all members from the database. Any authenticated user.',
    response_model=list[UserSchema],
    responses={
        status.HTTP_200_OK: {
            'model': list[UserSchema],
            'description': 'Members successfully retrieved.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': BadResponse,
            'description': 'An error occurred when you tried to retrieve members.',
        },
    },
)
@cache(
    expire=60,
    namespace=settings.cache.namespace.member,
    key_builder=custom_key_builder,
)
async def get_members(service: MemberServiceDep, current_user: CurrentCoachDep):
    return await service.get_users()


@router.get(
    '/members/{member_uuid}',
    summary='Get specific member by id',
    tags=[title],
    description='Get specific member from the database. Any authenticated user.',
    response_model=UserSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Member not found',
        }
    },
)
async def get_specific_member(member_uuid: UUID, service: MemberServiceDep, current_user: CurrentCoachDep):
    return await service.get_user(member_uuid)


@router.put(
    '/members/{member_uuid}',
    summary='Update specific member',
    tags=[title],
    description='Update specific member in the database. Coach only.',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Member successfully updated',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': BadResponse,
            'description': 'Coaches only',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Member not found',
        },
    },
)
async def update_member(
    member_uuid: UUID,
    member: UserRegisterSchema,
    service: MemberServiceDep,
    current_user: CurrentCoachDep,  # coach only
):
    return await service.update_user(member_uuid, member)


@router.delete(
    '/members/{member_uuid}',
    summary='Delete specific member',
    tags=[title],
    description='Delete specific member in the database. Coach only.',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Member successfully deleted',
        },
        status.HTTP_403_FORBIDDEN: {
            'model': BadResponse,
            'description': 'Coaches only',
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
async def delete_member(member_uuid: UUID, service: MemberServiceDep, current_user: CurrentCoachDep):  # coach only
    return await service.delete_user(member_uuid)
