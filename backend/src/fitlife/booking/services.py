from fastapi import HTTPException

from fitlife.booking.repositories import BookingRepository
from fitlife.schedule.repositories import ScheduleRepository


class BookingService:
    def __init__(self, booking_repo: BookingRepository, schedule_repo: ScheduleRepository):
        self.booking_repo = booking_repo
        self.schedule_repo = schedule_repo

    def create_booking(self, schedule_id: str, customer_id: str):
        schedule = self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")

        if schedule["participants_count"] >= schedule["max_participants"]:
            raise HTTPException(status_code=400, detail="Training is fully booked")

        booking = self.booking_repo.create({"customer_id": customer_id, "schedule_id": schedule_id})

        self.schedule_repo.increment_participants(schedule_id)
        return booking
