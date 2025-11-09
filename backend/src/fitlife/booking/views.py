from fastapi import APIRouter, Depends, status

from fitlife.booking.repositories import BookingRepository
from fitlife.booking.schemas import BookingCreate, BookingResponse
from fitlife.booking.services import BookingService
from fitlife.database import get_db
from fitlife.deps import get_current_customer
from fitlife.schedule.repositories import ScheduleRepository

router = APIRouter()


@router.post("", response_model=BookingResponse)
async def book_training(
        booking_data: BookingCreate,
        current_user: dict = Depends(get_current_customer),
        db: dict = Depends(get_db),
):
    booking_repo = BookingRepository(db)
    schedule_repo = ScheduleRepository(db)
    booking_service = BookingService(booking_repo, schedule_repo)

    booking = booking_service.create_booking(booking_data.schedule_id, current_user["id"])
    return booking


@router.get("", response_model=list[BookingResponse])
async def get_bookings_list(
        current_user: dict = Depends(get_current_customer),
        db: dict = Depends(get_db),
):
    booking_repo = BookingRepository(db)
    bookings = booking_repo.get_all()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(
        booking_id: str,
        current_user: dict = Depends(get_current_customer),
        db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    booking_repo = BookingRepository(db)
    booking = booking_repo.get_by_id(booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking
