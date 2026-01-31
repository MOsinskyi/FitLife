from sqlalchemy import Column, String

from fitlife.models import Base


class CoachModel(Base):
    __tablename__ = 'coaches'

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
