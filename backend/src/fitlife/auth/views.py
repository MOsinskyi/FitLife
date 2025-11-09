from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fitlife.auth.schemas import Token
from fitlife.auth.services import AuthService
from fitlife.database import get_db
from fitlife.user.repositories import UserRepository

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: dict = Depends(get_db),
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_token(user)

    return {"access_token": access_token, "token_type": "bearer"}
