from sqlalchemy import Column, String, ForeignKey, Table, UUID
from fitlife.models import Base

coach_specialization_table = Table(
    "coach_specialization",
    Base.metadata,
    Column(
        "coach_id",
        UUID(as_uuid=True),
        ForeignKey("coaches.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "specialization_id",
        UUID(as_uuid=True),
        ForeignKey("specializations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class SpecializationModel(Base):
    __tablename__ = "specializations"

    name = Column(String, nullable=False, unique=True)
    emoji = Column(String, nullable=False, default="⚡")

    def __str__(self):
        return f"{self.emoji} {self.name}"
