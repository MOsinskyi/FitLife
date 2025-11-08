from typing import Optional

from fitlife.user.schemas import UserCreate, UserResponse


class CoachCreate(UserCreate):
    specialization: Optional[str] = None
    bio: Optional[str] = None


class CoachResponse(UserResponse):
    specialization: Optional[str] = None
    bio: Optional[str] = None
