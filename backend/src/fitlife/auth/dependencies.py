from typing import Annotated, TypeVar
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

from fitlife.coach.models import CoachModel
from fitlife.database import SessionDep
from fitlife.member.models import MemberModel
from fitlife.security import SecurityDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

T = TypeVar('T', bound=DeclarativeBase)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
    security: SecurityDep,
) -> MemberModel | CoachModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    payload = security.decode_access_token(token)
    user_id: str | None = payload.get('sub')
    role: str | None = payload.get('role')

    if user_id is None or role is None:
        raise credentials_exception

    model = MemberModel if role == 'member' else CoachModel if role == 'coach' else None

    if model is None:
        raise credentials_exception

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception from None

    result = await session.execute(select(model).where(model.id == user_uuid))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_member(
    current_user: Annotated[MemberModel | CoachModel, Depends(get_current_user)],
) -> MemberModel:
    if not isinstance(current_user, MemberModel):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions',
        )
    return current_user


async def get_current_active_coach(
    current_user: Annotated[MemberModel | CoachModel, Depends(get_current_user)],
) -> CoachModel:
    if not isinstance(current_user, CoachModel):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions',
        )
    return current_user


CurrentUserDep = Annotated[MemberModel | CoachModel, Depends(get_current_user)]
CurrentMemberDep = Annotated[MemberModel, Depends(get_current_active_member)]
CurrentCoachDep = Annotated[CoachModel, Depends(get_current_active_coach)]
