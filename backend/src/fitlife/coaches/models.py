from sqlalchemy import Column, Integer, String

from fitlife.models import UserBase


class CoachModel(UserBase):
    __tablename__ = 'coaches'

    specialization = Column(
        String,
        nullable=False,
        default='',
    )
    emoji = Column(
        String,
        nullable=False,
        default='',
    )
    experience = Column(
        Integer,
        nullable=False,
        default=0,
    )
    experience_label = Column(
        String,
        nullable=False,
        default='',
    )
