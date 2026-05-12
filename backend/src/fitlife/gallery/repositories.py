from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.gallery.models import GalleryModel


class GalleryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[GalleryModel]:
        stmt = select(GalleryModel).order_by(
            GalleryModel.display_order.asc(), GalleryModel.created_at.desc()
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
