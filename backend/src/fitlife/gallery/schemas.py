from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class GalleryBase(BaseModel):
    image_url: str
    title: str = ''
    description: str = ''
    display_order: int = 0

class GalleryResponse(GalleryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
