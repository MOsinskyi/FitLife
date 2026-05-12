from fastapi import APIRouter
from fitlife.gallery.dependencies import GalleryServiceDep
from fitlife.gallery.schemas import GalleryResponse

gallery_router = APIRouter(prefix="/gallery", tags=["gallery"])


@gallery_router.get("", response_model=list[GalleryResponse])
async def get_gallery(service: GalleryServiceDep):
    return await service.get_all_images()
