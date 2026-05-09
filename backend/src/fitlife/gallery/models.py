from sqlalchemy import Column, String, Integer
from fitlife.models import Base

class GalleryModel(Base):
    __tablename__ = 'gallery'

    image_url = Column(String, nullable=False)
    title = Column(String, nullable=False, default='')
    description = Column(String, nullable=False, default='')
    display_order = Column(Integer, nullable=False, default=0)
