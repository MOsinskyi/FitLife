from uuid import UUID

from pydantic import BaseModel, Field

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
    username: str = Field(pattern=PHONE_PATTERN)
    password: str
