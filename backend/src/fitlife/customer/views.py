from fastapi import APIRouter, Depends, status

from fitlife.booking.repositories import BookingRepository
from fitlife.booking.schemas import StatsResponse
from fitlife.database import get_db
from fitlife.deps import get_current_customer
from fitlife.user.repositories import UserRepository
from fitlife.user.services import UserService
from fitlife.customer.schemas import CustomerCreate, CustomerResponse

router = APIRouter()


@router.post("/register", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def register_customer(
        customer: CustomerCreate,
        db: dict = Depends(get_db),
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    customer_data = customer.dict()
    new_customer = user_service.register_customer(customer_data)

    return {k: v for k, v in new_customer.items() if k != "hashed_password"}


@router.get("/me", response_model=CustomerResponse)
async def get_customer_profile(current_user: dict = Depends(get_current_customer)):
    return {k: v for k, v in current_user.items() if k != "hashed_password"}


@router.get("/me/stats", response_model=StatsResponse)
async def view_own_stats(
        current_user: dict = Depends(get_current_customer),
        db: dict = Depends(get_db),
):
    booking_repo = BookingRepository(db)
    customer_bookings = booking_repo.get_by_customer(current_user["id"])
    completed = [b for b in customer_bookings if b["status"] == "completed"]

    return StatsResponse(
        total_bookings=len(customer_bookings),
        completed_sessions=len(completed),
        active_membership=None,
        visit_count=current_user.get("visit_count", 0)
    )
