from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fitlife.database import get_session
from fitlife.gallery.repositories import GalleryRepository
from fitlife.gallery.services import GalleryService


async def get_gallery_repository(
    session: AsyncSession = Depends(get_session),
) -> GalleryRepository:
    return GalleryRepository(session)


async def get_gallery_service(
    repository: GalleryRepository = Depends(get_gallery_repository),
) -> GalleryService:
    return GalleryService(repository)


GalleryServiceDep = Annotated[GalleryService, Depends(get_gallery_service)]
