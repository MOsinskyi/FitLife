import uuid
from datetime import UTC, datetime


class BookingRepository:
    def __init__(self, db: dict):
        self.bookings_db = db["bookings"]

    def create(self, booking_data: dict) -> dict:
        booking_id = str(uuid.uuid4())
        booking = {
            "id": booking_id,
            **booking_data,
            "booking_time": datetime.now(UTC),
            "status": "confirmed",
        }
        self.bookings_db[booking_id] = booking
        return booking

    def get_by_id(self, booking_id: str) -> dict | None:
        return self.bookings_db.get(booking_id)

    def get_all(self) -> list[dict]:
        return list(self.bookings_db.values())

    def get_by_customer(self, customer_id: str) -> list[dict]:
        return [b for b in self.bookings_db.values() if b["customer_id"] == customer_id]

    def get_by_schedule(self, schedule_id: str) -> list[dict]:
        return [b for b in self.bookings_db.values() if b["schedule_id"] == schedule_id]
