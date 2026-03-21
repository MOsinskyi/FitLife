from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from fitlife.models import UserBase


class CoachModel(UserBase):
    __tablename__ = 'coaches'

    speciality = Column(
        String,
        nullable=False,
        server_default='Силові тренування',
    )

    emoji_char = Column(
        String,
        nullable=False,
        server_default='🏋️',
    )

    experience = Column(
        Integer,
        nullable=False,
        default=1,
        server_default='1',
        comment='Потрібно ввести досвід в роках',
    )

    experience_title = Column(
        String,
        nullable=False,
        default='рік',
        server_default='рік',
    )

    sessions = relationship(
        'TrainingSessionModel',
        back_populates='coach',
    )
