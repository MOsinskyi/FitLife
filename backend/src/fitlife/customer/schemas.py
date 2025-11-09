from fitlife.user.schemas import UserCreate, UserResponse


class CustomerCreate(UserCreate):
    pass


class CustomerResponse(UserResponse):
    membership_id: str | None = None
    visit_count: int = 0
