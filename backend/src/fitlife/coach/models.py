from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from fitlife.models import UserBase


class CoachModel(UserBase):
    __tablename__ = 'coaches'

    speciality = Column(
        String,
        nullable=False,
        server_default='Силові тренування',
        name='Спеціальність',
    )

    emoji_entity = Column(
        String,
        nullable=False,
        server_default='&#x1F3CB;',
        name='Emoji',
        comment='HTML entity (hex)',
    )

    experience = Column(
        Integer,
        nullable=False,
        default=1,
        server_default='1',
        name='Досвід',
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
