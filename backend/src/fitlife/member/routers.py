from uuid import UUID

from fastapi import APIRouter
from starlette import status

from fitlife.member.dependencies import MemberServiceDep
from fitlife.member.schemas import MemberAddSchema, MemberSchema
from fitlife.schemas import BadResponse, OkResponse

router = APIRouter()

title = '👨‍👩‍ Members'


@router.post(
    '/members',
    summary='Add new member',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    description='Add new member to the database',
    responses={
        status.HTTP_201_CREATED: {
            'model': OkResponse,
            'description': 'Member successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Member with phone number already exists',
        },
    },
)
async def add_member(member: MemberAddSchema, service: MemberServiceDep):
    return await service.create_member(member)


@router.get(
    '/members',
    summary='Get all members',
    tags=[title],
    description='Get all members from the database',
    response_model=list[MemberSchema],
)
async def get_members(service: MemberServiceDep):
    return await service.get_members()


@router.get(
    '/members/{member_uuid}',
    summary='Get specific member by index',
    tags=[title],
    description='Get specific member from the database',
    response_model=MemberSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Member not found',
        }
    },
)
async def get_specific_member(member_uuid: UUID, service: MemberServiceDep):
    return await service.get_member(member_uuid)


@router.put(
    '/members/{member_uuid}',
    summary='Update specific member',
    tags=[title],
    description='Update specific member in the database',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Member successfully updated',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Member not found',
        },
    },
)
async def update_member(member_uuid: UUID, member: MemberAddSchema, service: MemberServiceDep):
    return await service.update_member(member_uuid, member)


@router.delete(
    '/members/{member_uuid}',
    summary='Delete specific member',
    tags=[title],
    description='Delete specific member in the database',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Member successfully deleted',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Member not found',
        },
    },
)
async def delete_member(member_uuid: UUID, service: MemberServiceDep):
    await service.delete_member(member_uuid)
    return OkResponse(msg='Member successfully deleted!')
