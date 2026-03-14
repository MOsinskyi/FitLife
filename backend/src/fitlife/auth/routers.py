from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from fitlife.auth.dependencies import CurrentUserDep
from fitlife.auth.schemas import (
    CoachRegisterSchema,
    LoginSchema,
    MemberRegisterSchema,
    TokenSchema,
    UserResponseSchema,
)
from fitlife.coach.models import CoachModel
from fitlife.config import settings
from fitlife.database import SessionDep
from fitlife.member.models import MemberModel
from fitlife.schemas import BadResponse
from fitlife.security import SecurityDep

router = APIRouter()

title = '🔐 Authentication'


@router.post(
    '/auth/register/member',
    summary='Register new member',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    responses={
        status.HTTP_201_CREATED: {
            'model': UserResponseSchema,
            'description': 'Member successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Member with phone number already exists',
        },
    },
)
async def register_member(
    member_data: MemberRegisterSchema,
    session: SessionDep,
    security: SecurityDep,
) -> UserResponseSchema:
    result = await session.execute(select(MemberModel).where(MemberModel.phone_number == member_data.phone_number))
    existing_member = result.scalar_one_or_none()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Member with this phone number already exists',
        )

    new_member = MemberModel(
        first_name=member_data.first_name,
        last_name=member_data.last_name,
        email=member_data.email,
        phone_number=member_data.phone_number,
        password=security.hash_password(member_data.password),
        role='member',
    )
    session.add(new_member)
    await session.commit()
    await session.refresh(new_member)

    return UserResponseSchema(
        id=new_member.id,
        first_name=str(new_member.first_name),
        last_name=str(new_member.last_name),
        email=new_member.email,
        phone_number=str(new_member.phone_number),
        role=str(new_member.role),
    )


@router.post(
    '/auth/register/coach',
    summary='Register new coach',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    responses={
        status.HTTP_201_CREATED: {
            'model': UserResponseSchema,
            'description': 'Coach successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Coach with phone number already exists',
        },
    },
)
async def register_coach(
    coach_data: CoachRegisterSchema,
    session: SessionDep,
    security: SecurityDep,
) -> UserResponseSchema:
    result = await session.execute(select(CoachModel).where(CoachModel.phone_number == coach_data.phone_number))
    existing_coach = result.scalar_one_or_none()
    if existing_coach:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Coach with this phone number already exists',
        )

    new_coach = CoachModel(
        first_name=coach_data.first_name,
        last_name=coach_data.last_name,
        email=coach_data.email,
        phone_number=coach_data.phone_number,
        password=security.hash_password(coach_data.password),
        role='coach',
    )
    session.add(new_coach)
    await session.commit()
    await session.refresh(new_coach)

    return UserResponseSchema(
        id=new_coach.id,
        first_name=str(new_coach.first_name),
        last_name=str(new_coach.last_name),
        email=new_coach.email,
        phone_number=str(new_coach.phone_number),
        role=str(new_coach.role),
    )


@router.post(
    '/auth/login',
    summary='Login user',
    tags=[title],
    responses={
        status.HTTP_200_OK: {
            'model': TokenSchema,
            'description': 'Successfully logged in',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': BadResponse,
            'description': 'Invalid credentials',
        },
    },
)
async def login(credentials: LoginSchema, session: SessionDep, security: SecurityDep) -> TokenSchema:
    result = await session.execute(
        select(MemberModel)
        .options(selectinload(MemberModel.sessions))
        .where(MemberModel.phone_number == credentials.phone_number),
    )
    user = result.scalar_one_or_none()
    user_type = 'member'

    if user is None:
        result = await session.execute(
            select(CoachModel)
            .options(selectinload(CoachModel.sessions))
            .where(CoachModel.phone_number == credentials.phone_number),
        )
        user = result.scalar_one_or_none()
        user_type = 'coach'

    if user is None or not security.verify_password(credentials.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid phone number or password',
        )

    access_token_expires = timedelta(minutes=settings.security.access_token_expire_minutes)
    access_token = security.create_access_token(
        data={'sub': str(user.id), 'role': user_type}, expires_delta=access_token_expires
    )

    return TokenSchema(access_token=access_token)


@router.get(
    '/auth/me',
    summary='Get current user',
    tags=[title],
    response_model=UserResponseSchema,
    responses={
        status.HTTP_200_OK: {
            'model': UserResponseSchema,
            'description': 'Successfully retrieved current user',
        },
    },
)
async def get_current_user_endpoint(current_user: CurrentUserDep) -> UserResponseSchema:
    user_data = {
        'id': current_user.id,
        'first_name': str(current_user.first_name) if current_user.first_name else '',
        'last_name': str(current_user.last_name) if current_user.last_name else '',
        'email': current_user.email,
        'phone_number': str(current_user.phone_number) if current_user.phone_number else '',
        'role': str(current_user.role) if current_user.role else '',
    }
    return UserResponseSchema(**user_data)
