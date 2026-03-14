from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from fitlife.schemas import PHONE_PATTERN


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID | None = None
    role: str | None = None


class LoginSchema(BaseModel):
    phone_number: str = Field(pattern=PHONE_PATTERN)
    password: str


class MemberRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str = Field(pattern=PHONE_PATTERN)
    password: str


class CoachRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str = Field(pattern=PHONE_PATTERN)
    password: str


class UserResponseSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str = Field(pattern=PHONE_PATTERN)
    role: str
