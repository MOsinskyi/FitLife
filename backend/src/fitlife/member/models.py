from sqlalchemy.orm import relationship

from fitlife.models import UserBase
from fitlife.training_session.models import session_participants


class MemberModel(UserBase):
    __tablename__ = 'members'

    sessions = relationship(
        'TrainingSessionModel',
        secondary=session_participants,
        back_populates='members',
    )
