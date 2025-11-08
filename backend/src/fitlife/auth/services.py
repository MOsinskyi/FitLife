from datetime import timedelta

from fastapi import HTTPException, status

from fitlife.config import settings
from fitlife.user.repositories import UserRepository
from fitlife.security import verify_password, create_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_token(self, user: dict) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": user["email"], "role": user["role"]},
            expires_delta=access_token_expires
        )
