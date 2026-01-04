from pydantic import BaseModel


class OkResponse(BaseModel):
    success: bool = True
    msg: str
    data: BaseModel | None = None


class BadResponse(BaseModel):
    success: bool = False
    msg: str
    data: BaseModel | None = None
