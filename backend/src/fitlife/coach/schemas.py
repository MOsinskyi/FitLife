from fitlife.user.schemas import UserCreate, UserResponse


class CoachCreate(UserCreate):
    specialization: str | None = None
    bio: str | None = None


class CoachResponse(UserResponse):
    specialization: str | None = None
    bio: str | None = None
