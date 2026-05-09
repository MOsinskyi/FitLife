from fitlife.gallery.repositories import GalleryRepository
from fitlife.gallery.schemas import GalleryResponse

class GalleryService:
    def __init__(self, repository: GalleryRepository):
        self.repository = repository

    async def get_all_images(self) -> list[GalleryResponse]:
        images = await self.repository.get_all()
        return [GalleryResponse.model_validate(img) for img in images]
