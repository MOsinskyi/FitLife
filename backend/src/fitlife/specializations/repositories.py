from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.specializations.models import SpecializationModel
from uuid import UUID


class SpecializationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[SpecializationModel]:
        stmt = select(SpecializationModel).order_by(SpecializationModel.name.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_ids(self, ids: list[UUID]) -> list[SpecializationModel]:
        stmt = select(SpecializationModel).where(SpecializationModel.id.in_(ids))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
