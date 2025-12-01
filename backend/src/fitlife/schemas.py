from pydantic import BaseModel


class OkResponse(BaseModel):
    success: bool = True
    msg: str


class BadResponse(BaseModel):
    success: bool = False
    msg: str
