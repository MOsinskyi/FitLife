from typing import override
from uuid import UUID

from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from fitlife.coaches.models import CoachModel
from fitlife.config import settings
from fitlife.database import new_session
from fitlife.schemas import UserRoles
from fitlife.security import Security


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get('username')
        password = form.get('password')

        if not email or not password:
            return False

        async with new_session() as session:
            coach = await self._get_coach_by_email(session, email)

            if not coach:
                return False

            if not Security.verify_password(password, coach.password):
                return False

            token = Security.create_access_token(data={'sub': str(coach.id), 'email': coach.email, 'role': coach.role})

            request.session.update({'token': token})

        return True

    @override
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get('token')

        if not token:
            return False

        payload = Security.decode_access_token(token)
        if not payload or payload.get('role') != UserRoles.COACH.value:
            return False

        user_id = UUID(payload.get('sub'))
        if not user_id:
            return False

        async with new_session() as session:
            coach = await self._get_coach_by_id(session, user_id)
            if not coach:
                return False

        return True

    @staticmethod
    async def _get_coach_by_email(session: AsyncSession, email: str) -> CoachModel | None:
        stmt = select(CoachModel).where(CoachModel.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _get_coach_by_id(session: AsyncSession, coach_id: UUID) -> CoachModel | None:
        stmt = select(CoachModel).where(CoachModel.id == coach_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


authentication_backend = AdminAuth(secret_key=settings.security.secret_key)
