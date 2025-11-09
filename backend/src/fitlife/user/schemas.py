from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime
