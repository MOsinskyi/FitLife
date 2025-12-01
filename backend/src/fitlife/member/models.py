from sqlalchemy.orm import Mapped

from fitlife.models import Base


class MemberModel(Base):
    __tablename__ = 'members'

    name: Mapped[str]
    phone: Mapped[str]
