from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.exc import InvalidTokenError

from fitlife.exceptions import InvalidCredentialsException
from fitlife.members.dependencies import MemberRepositoryDep
from fitlife.models import UserBase
from fitlife.security import SecurityDep

from ..coaches.dependencies import CoachRepositoryDep
from ..schemas import UserRoles
from .services import AuthService

if TYPE_CHECKING:
    pass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_authentication_service(
    member_repository: MemberRepositoryDep,
    coach_repository: CoachRepositoryDep,
    security: SecurityDep,
):
    return AuthService(member_repository, coach_repository, security)


async def get_current_user(
    member_repository: MemberRepositoryDep,
    coach_repository: CoachRepositoryDep,
    security: SecurityDep,
    token: str = Depends(oauth2_scheme),
) -> 'UserBase':
    try:
        payload = security.decode_access_token(token)
        user_id: str = payload.get('sub')
        role: str = payload.get('role')

        if user_id is None or role is None:
            raise InvalidCredentialsException('Invalid token')

    except InvalidTokenError:
        raise InvalidCredentialsException('Invalid token') from None

    if role == UserRoles.MEMBER.value:
        user = await member_repository.get_user_by_id(UUID(user_id))
    elif role == UserRoles.COACH.value:
        user = await coach_repository.get_user_by_id(UUID(user_id))
    else:
        raise InvalidCredentialsException('Invalid role')

    if user is None:
        raise InvalidCredentialsException('Invalid credentials')

    return user


CurrentUserDep = Annotated[UserBase, Depends(get_current_user)]

AuthServiceDep = Annotated[AuthService, Depends(get_authentication_service)]
