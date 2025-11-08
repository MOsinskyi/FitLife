import uuid
from datetime import datetime
from typing import Dict, List


class BookingRepository:
    def __init__(self, db: dict):
        self.bookings_db = db["bookings"]

    def create(self, booking_data: dict) -> Dict:
        booking_id = str(uuid.uuid4())
        booking = {
            "id": booking_id,
            **booking_data,
            "booking_time": datetime.utcnow(),
            "status": "confirmed"
        }
        self.bookings_db[booking_id] = booking
        return booking

    def get_by_customer(self, customer_id: str) -> List[Dict]:
        return [b for b in self.bookings_db.values() if b["customer_id"] == customer_id]

    def get_by_schedule(self, schedule_id: str) -> List[Dict]:
        return [b for b in self.bookings_db.values() if b["schedule_id"] == schedule_id]
