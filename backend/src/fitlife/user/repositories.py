import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List


class UserRepository:
    def __init__(self, db: dict):
        self.accounts_db = db["accounts"]
        self.coaches_db = db["coaches"]
        self.customers_db = db["customers"]

    def get_by_email(self, email: str) -> Optional[Dict]:
        return self.accounts_db.get(email)

    def get_by_id(self, user_id: str, role: str) -> Optional[Dict]:
        if role == "coach":
            return self.coaches_db.get(user_id)
        elif role == "customer":
            return self.customers_db.get(user_id)
        elif role == "manager":
            # Search for manager in accounts_db
            for account in self.accounts_db.values():
                if account.get("id") == user_id and account.get("role") == "manager":
                    return account
        return None

    def create_coach(self, coach_data: dict) -> Dict:
        coach_id = str(uuid.uuid4())
        coach = {
            "id": coach_id,
            **coach_data,
            "role": "coach",
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        self.accounts_db[coach_data["email"]] = coach
        self.coaches_db[coach_id] = coach
        return coach

    def create_customer(self, customer_data: dict) -> Dict:
        customer_id = str(uuid.uuid4())
        customer = {
            "id": customer_id,
            **customer_data,
            "role": "customer",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "membership_id": None,
            "visit_count": 0
        }
        self.accounts_db[customer_data["email"]] = customer
        self.customers_db[customer_id] = customer
        return customer

    def get_all_coaches(self) -> List[Dict]:
        return list(self.coaches_db.values())

    def get_all_customers(self) -> List[Dict]:
        return list(self.customers_db.values())

    def get_all_managers(self) -> List[Dict]:
        return [account for account in self.accounts_db.values() if account.get("role") == "manager"]

    def update_customer_visits(self, customer_id: str) -> Dict:
        customer = self.customers_db.get(customer_id)
        if customer:
            customer["visit_count"] = customer.get("visit_count", 0) + 1
        return customer
