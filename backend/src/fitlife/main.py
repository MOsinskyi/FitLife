from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class MemberSchema(BaseModel):
    name: str
    phone: str


members = []


@app.post("/members")
def add_member(member: MemberSchema):
    members.append(member)


@app.get("/members")
def get_members():
    return members
