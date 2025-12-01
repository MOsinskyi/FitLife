import enum
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MembershipTypes(enum.Enum):
    DISPOSABLE = 'Disposable'
    MONTHLY = 'Monthly'
    ANNUAL = 'Annual'


class MembershipAddSchema(BaseModel):
    type: MembershipTypes
    fee: Decimal = Field(decimal_places=2, max_digits=4)


class MembershipSchema(MembershipAddSchema):
    id: UUID = Field(default_factory=uuid4)
