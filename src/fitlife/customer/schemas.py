from typing import Optional

from fitlife.user.schemas import UserCreate, UserResponse


class CustomerCreate(UserCreate):
    pass


class CustomerResponse(UserResponse):
    membership_id: Optional[str] = None
    visit_count: int = 0
