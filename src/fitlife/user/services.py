from fastapi import HTTPException
from fitlife.security import get_password_hash
from fitlife.user.repositories import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_coach(self, coach_data: dict):
        if self.user_repo.get_by_email(coach_data["email"]):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(coach_data.pop("password"))
        coach_data["hashed_password"] = hashed_password

        return self.user_repo.create_coach(coach_data)

    def register_customer(self, customer_data: dict):
        if self.user_repo.get_by_email(customer_data["email"]):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(customer_data.pop("password"))
        customer_data["hashed_password"] = hashed_password

        return self.user_repo.create_customer(customer_data)
