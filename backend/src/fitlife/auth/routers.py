from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from fitlife.auth.dependencies import CurrentUserDep
from fitlife.auth.schemas import (
    CoachRegisterSchema,
    MemberRegisterSchema,
    RefreshTokenSchema,
    TokenPairSchema,
    UserResponseSchema,
)
from fitlife.coach.dependencies import CoachServiceDep
from fitlife.coach.models import CoachModel
from fitlife.config import settings
from fitlife.database import SessionDep
from fitlife.member.dependencies import MemberServiceDep
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
            'model': TokenPairSchema,
            'description': 'Successfully logged in — returns access + refresh tokens',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': BadResponse,
            'description': 'Invalid credentials',
        },
    },
)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    security: SecurityDep,
    member_service: MemberServiceDep,
    coach_service: CoachServiceDep,
) -> TokenPairSchema:
    user = await member_service.get_user_by_phone_number(credentials.username)
    user_type = 'member'

    if user is None:
        user = await coach_service.get_user_by_phone_number(credentials.username)
        user_type = 'coach'

    if user is None or not security.verify_password(credentials.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid phone number or password',
        )

    token_data = {'sub': str(user.id), 'role': user_type}

    access_token = security.create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.security.access_token_expire_minutes),
    )
    refresh_token = security.create_refresh_token(data=token_data)

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/auth/token/refresh',
    summary='Refresh access token',
    tags=[title],
    responses={
        status.HTTP_200_OK: {
            'model': TokenPairSchema,
            'description': 'New access + refresh token pair (old refresh token is invalidated by rotation)',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'model': BadResponse,
            'description': 'Invalid or expired refresh token',
        },
    },
)
async def refresh_token(body: RefreshTokenSchema, security: SecurityDep) -> TokenPairSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or expired refresh token',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    payload = security.decode_refresh_token(body.refresh_token)
    user_id: str | None = payload.get('sub')
    role: str | None = payload.get('role')

    if not user_id or not role:
        raise credentials_exception

    token_data = {'sub': user_id, 'role': role}

    new_access_token = security.create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.security.access_token_expire_minutes),
    )
    new_refresh_token = security.create_refresh_token(data=token_data)

    return TokenPairSchema(access_token=new_access_token, refresh_token=new_refresh_token)


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
