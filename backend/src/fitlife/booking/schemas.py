from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    schedule_id: str


class BookingResponse(BaseModel):
    id: str
    customer_id: str
    schedule_id: str
    booking_time: datetime
    status: str = "confirmed"


class VisitRecordResponse(BaseModel):
    id: str
    customer_id: str
    visit_time: datetime
    marked_by: str


class StatsResponse(BaseModel):
    total_bookings: int
    completed_sessions: int
    active_membership: dict | None = None
    visit_count: int
