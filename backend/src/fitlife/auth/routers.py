from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fitlife.exceptions import InvalidCredentialsException

from ..schemas import UserSchema
from .dependencies import AuthServiceDep, CurrentUserDep
from .schemas import TokenSchema

auth_router = APIRouter(prefix="/auth", tags=["✅ Authentication"])


@auth_router.post(
    "/login",
    response_model=TokenSchema,
    responses={
        status.HTTP_200_OK: {
            "description": "Success",
            "model": TokenSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def login(
    auth_service: AuthServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
):
    try:
        return await auth_service.authenticate_user(
            phone_number=form_data.username,
            password=form_data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail=str(e),
        ) from e


@auth_router.get(
    "/me",
    response_model=UserSchema,
    responses={
        status.HTTP_200_OK: {
            "description": "Success",
            "model": UserSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
)
async def read_users_me(current_user: CurrentUserDep):
    try:
        return current_user
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail=str(e),
        ) from e
