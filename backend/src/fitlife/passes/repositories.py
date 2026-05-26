from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.passes.models import PassModel, PassFeatureModel

class PassRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_active(self) -> list[PassModel]:
        stmt = select(PassModel).where(PassModel.is_active == True).order_by(PassModel.price.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, pass_id: UUID) -> PassModel | None:
        stmt = select(PassModel).where(PassModel.id == pass_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

class PassFeatureRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_ids(self, feature_ids: list[UUID]) -> list[PassFeatureModel]:
        stmt = select(PassFeatureModel).where(PassFeatureModel.id.in_(feature_ids))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all(self) -> list[PassFeatureModel]:
        stmt = select(PassFeatureModel)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
