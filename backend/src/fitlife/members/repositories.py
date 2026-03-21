from uuid import UUID

from sqlalchemy import delete, select, update

from fitlife.repositories import BaseUserRepository

from ..schemas import UserUpdateSchema
from .models import MemberModel


class MemberRepository(BaseUserRepository[MemberModel]):
    async def get_user_by_id(self, user_id: UUID) -> MemberModel | None:
        stmt = select(MemberModel).where(MemberModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: MemberModel) -> MemberModel | None:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_users(self) -> list[MemberModel]:
        smtp = select(MemberModel)
        result = await self.session.execute(smtp)
        return list(result.scalars().all())

    async def update_user(self, user_id: UUID, data: UserUpdateSchema) -> MemberModel | None:
        smtp = (
            update(MemberModel)
            .where(MemberModel.id == user_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(MemberModel)
        )
        result = await self.session.execute(smtp)
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: UUID) -> None:
        stmt = delete(MemberModel).where(MemberModel.id == user_id)
        await self.session.execute(stmt)
