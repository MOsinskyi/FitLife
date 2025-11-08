from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MembershipTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    duration_days: int
    price: float


class MembershipTypeResponse(MembershipTypeCreate):
    id: str


class CustomerMembershipResponse(BaseModel):
    id: str
    customer_id: str
    membership_type_id: str
    start_date: datetime
    end_date: datetime
    is_active: bool = True
