from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey, UUID
from sqlalchemy.orm import Mapped, relationship
from fitlife.models import Base

pass_feature_association = Table(
    "pass_feature_association",
    Base.metadata,
    Column(
        "pass_id",
        UUID(as_uuid=True),
        ForeignKey("passes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "feature_id",
        UUID(as_uuid=True),
        ForeignKey("pass_features.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

class PassFeatureModel(Base):
    __tablename__ = "pass_features"

    name = Column(String, nullable=False, unique=True)

    def __str__(self):
        return self.name

class PassModel(Base):
    __tablename__ = "passes"

    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    features: Mapped[list["PassFeatureModel"]] = relationship(
        secondary=pass_feature_association,
        lazy="selectin",
    )
