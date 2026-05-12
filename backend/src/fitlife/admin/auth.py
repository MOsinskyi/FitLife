from typing import override
from uuid import UUID

from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from fitlife.admin.models import AdminModel
from fitlife.config import settings
from fitlife.database import new_session
from fitlife.schemas import UserRoles
from fitlife.security import Security


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        async with new_session() as session:
            admin = await self._get_admin_by_email(session, email)

            if not admin:
                return False

            if not Security.verify_password(password, admin.password):
                return False

            token = Security.create_access_token(
                data={"sub": str(admin.id), "email": admin.email, "role": admin.role}
            )

            request.session.update({"token": token})

        return True

    @override
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        payload = Security.decode_access_token(token)
        if not payload or payload.get("role") != UserRoles.ADMIN.value:
            return False

        user_id = UUID(payload.get("sub"))
        if not user_id:
            return False

        async with new_session() as session:
            admin = await self._get_admin_by_id(session, user_id)
            if not admin:
                return False

        return True

    @staticmethod
    async def _get_admin_by_email(
        session: AsyncSession, email: str
    ) -> AdminModel | None:
        stmt = select(AdminModel).where(AdminModel.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _get_admin_by_id(
        session: AsyncSession, admin_id: UUID
    ) -> AdminModel | None:
        stmt = select(AdminModel).where(AdminModel.id == admin_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


authentication_backend = AdminAuth(secret_key=settings.security.secret_key)
