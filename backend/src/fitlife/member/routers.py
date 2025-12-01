from uuid import UUID

from fastapi import APIRouter
from sqlalchemy import exists, select
from starlette import status

from fitlife.database import SessionDep, add_entity, delete_entity, get_all_entities, get_entity_by_uuid, update_entity
from fitlife.member.models import MemberModel
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
async def add_member(member: MemberAddSchema, session: SessionDep):
    new_member = MemberModel(
        name=member.name,
        phone=member.phone,
    )

    phone_exists = await session.scalar(select(exists().where(MemberModel.phone == new_member.phone)))

    await add_entity(new_member, session, 'Member with the phone already exists', phone_exists)

    return OkResponse(msg='Member successfully added!')


@router.get(
    '/members',
    summary='Get all members',
    tags=[title],
    description='Get all members from the database',
    response_model=list[MemberSchema],
)
async def get_members(session: SessionDep):
    result = await get_all_entities(MemberModel, session)
    return result


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
async def get_specific_member(member_uuid: UUID, session: SessionDep):
    result = await get_entity_by_uuid(MemberModel, member_uuid, session, 'Member not found!')
    return result


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
async def update_member(member_uuid: UUID, member: MemberAddSchema, session: SessionDep):
    exiting_member = await get_entity_by_uuid(MemberModel, member_uuid, session, 'Member not found!')

    for field, value in member.model_dump(exclude_unset=True).items():
        setattr(exiting_member, field, value)

    await update_entity(exiting_member, session)

    return OkResponse(msg='Member successfully updated!')


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
async def delete_member(member_uuid: UUID, session: SessionDep):
    exiting_member = await get_entity_by_uuid(MemberModel, member_uuid, session, 'Member not found!')

    await delete_entity(exiting_member, session)

    return OkResponse(msg='Member successfully deleted!')
