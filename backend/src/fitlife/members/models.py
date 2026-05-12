from sqlalchemy.orm import Mapped, relationship

from fitlife.models import UserBase
from fitlife.training_sessions.models import SessionParticipant


class MemberModel(UserBase):
    __tablename__ = "members"

    participations: Mapped[list["SessionParticipant"]] = relationship(
        back_populates="member"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
