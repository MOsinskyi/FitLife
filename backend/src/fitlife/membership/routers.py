from uuid import UUID

from fastapi import APIRouter
from sqlalchemy import exists, select
from starlette import status

from fitlife.database import SessionDep, add_entity, get_all_entities, get_entity_by_uuid
from fitlife.membership.models import MembershipModel
from fitlife.membership.schemas import MembershipAddSchema, MembershipSchema
from fitlife.schemas import BadResponse, OkResponse

router = APIRouter()

title = '🪪 Memberships'


@router.post(
    '/memberships',
    summary='Add new membership',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    description='Add new membership to the database',
    responses={
        status.HTTP_201_CREATED: {
            'model': OkResponse,
            'description': 'Membership successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Membership already exists',
        },
    },
)
async def add_membership(membership: MembershipAddSchema, session: SessionDep):
    new_membership = MembershipModel(
        type=membership.type,
        fee=membership.fee,
    )

    membership_exists = await session.scalar(select(exists().where(MembershipModel.type == new_membership.type)))

    await add_entity(new_membership, session, 'Membership already exists', membership_exists)

    return OkResponse(msg='Membership successfully added!')


@router.get(
    '/memberships',
    summary='Get all memberships',
    tags=[title],
    description='Get all memberships from the database',
    response_model=list[MembershipSchema],
)
async def get_memberships(session: SessionDep):
    result = await get_all_entities(MembershipModel, session)
    return result


@router.get(
    '/memberships/{membership_uuid}',
    summary='Get specific membership by index',
    tags=[title],
    description='Get specific membership from the database',
    response_model=MembershipSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Membership not found',
        }
    },
)
async def get_specific_membership(membership_uuid: UUID, session: SessionDep):
    result = await get_entity_by_uuid(MembershipModel, membership_uuid, session, 'Membership not found!')
    return result
