from decimal import Decimal

from sqlalchemy.orm import Mapped

from fitlife.membership.schemas import MembershipTypes
from fitlife.models import Base


class MembershipModel(Base):
    __tablename__ = 'memberships'

    type: Mapped[MembershipTypes]
    fee: Mapped[Decimal]
