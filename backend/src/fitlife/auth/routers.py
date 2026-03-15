from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fitlife.auth.dependencies import CurrentUserDep
from fitlife.auth.schemas import (
    RefreshTokenSchema,
    TokenPairSchema,
)
from fitlife.coach.dependencies import CoachServiceDep
from fitlife.config import settings
from fitlife.member.dependencies import MemberServiceDep
from fitlife.schemas import BadResponse, UserRegisterSchema, UserSchema
from fitlife.security import SecurityDep

router = APIRouter()

title = '🔐 Authentication'


@router.post(
    '/auth/register/member',
    summary='Register new member',
    status_code=status.HTTP_200_OK,
    tags=[title],
    responses={
        status.HTTP_200_OK: {
            'model': UserSchema,
            'description': 'Member successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Member with phone number already exists',
        },
    },
)
async def register_member(
    member_data: UserRegisterSchema,
    member_service: MemberServiceDep,
):
    return await member_service.create_member(member_data)


@router.post(
    '/auth/register/coach',
    summary='Register new coach',
    status_code=status.HTTP_200_OK,
    tags=[title],
    responses={
        status.HTTP_200_OK: {
            'model': UserSchema,
            'description': 'Coach successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Coach with phone number already exists',
        },
    },
)
async def register_coach(
    coach_data: UserRegisterSchema,
    coach_service: CoachServiceDep,
) -> UserSchema:
    return await coach_service.create_coach(coach_data)


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
    response_model=UserSchema,
    responses={
        status.HTTP_200_OK: {
            'model': UserSchema,
            'description': 'Successfully retrieved current user',
        },
    },
)
async def get_current_user_endpoint(current_user: CurrentUserDep) -> UserSchema:
    user_data = {
        'id': current_user.id,
        'first_name': str(current_user.first_name) if current_user.first_name else '',
        'last_name': str(current_user.last_name) if current_user.last_name else '',
        'email': current_user.email,
        'phone_number': str(current_user.phone_number) if current_user.phone_number else '',
        'role': str(current_user.role) if current_user.role else '',
    }
    return UserSchema(**user_data)
