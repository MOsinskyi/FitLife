import uuid
from datetime import UTC, datetime
from typing import Any


class UserRepository:
    def __init__(self, db: dict[str, Any]):
        self.accounts_db: dict[str, Any] = db["accounts"]
        self.coaches_db: dict[str, Any] = db["coaches"]
        self.customers_db: dict[str, Any] = db["customers"]

    def get_by_email(self, email: str) -> dict[Any, Any] | None:
        result: dict[Any, Any] | None = self.accounts_db.get(email)
        return result

    def get_by_id(self, user_id: str, role: str) -> dict[Any, Any] | None:
        if role == "coach":
            result: dict[Any, Any] | None = self.coaches_db.get(user_id)
            return result
        elif role == "customer":
            result = self.customers_db.get(user_id)
            return result
        elif role == "manager":
            # Search for manager in accounts_db
            for account in self.accounts_db.values():
                if account.get("id") == user_id and account.get("role") == "manager":
                    account_result: dict[Any, Any] = account
                    return account_result
        return None

    def create_coach(self, coach_data: dict) -> dict:
        coach_id = str(uuid.uuid4())
        coach = {
            "id": coach_id,
            **coach_data,
            "role": "coach",
            "is_active": True,
            "created_at": datetime.now(UTC),
        }
        self.accounts_db[coach_data["email"]] = coach
        self.coaches_db[coach_id] = coach
        return coach

    def create_customer(self, customer_data: dict) -> dict:
        customer_id = str(uuid.uuid4())
        customer = {
            "id": customer_id,
            **customer_data,
            "role": "customer",
            "is_active": True,
            "created_at": datetime.now(UTC),
            "membership_id": None,
            "visit_count": 0,
        }
        self.accounts_db[customer_data["email"]] = customer
        self.customers_db[customer_id] = customer
        return customer

    def get_all_coaches(self) -> list[dict]:
        return list(self.coaches_db.values())

    def get_all_customers(self) -> list[dict]:
        return list(self.customers_db.values())

    def get_all_managers(self) -> list[dict]:
        return [
            account for account in self.accounts_db.values() if account.get("role") == "manager"
        ]

    def update_customer_visits(self, customer_id: str) -> dict[Any, Any]:
        customer: dict[Any, Any] | None = self.customers_db.get(customer_id)
        if customer:
            customer["visit_count"] = customer.get("visit_count", 0) + 1
            return customer
        return {}
