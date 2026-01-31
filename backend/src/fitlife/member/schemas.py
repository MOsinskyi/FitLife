from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from fitlife.schemas import PHONE_PATTERN


class MemberAddSchema(BaseModel):
    name: str
    phone: str = Field(pattern=PHONE_PATTERN)


class MemberSchema(MemberAddSchema):
    id: UUID = Field(default_factory=uuid4)
