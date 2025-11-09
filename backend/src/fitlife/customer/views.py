from fastapi import APIRouter, Depends, status

from fitlife.booking.repositories import BookingRepository
from fitlife.booking.schemas import StatsResponse
from fitlife.customer.schemas import CustomerCreate, CustomerResponse
from fitlife.database import get_db
from fitlife.deps import get_current_customer
from fitlife.user.repositories import UserRepository
from fitlife.user.services import UserService

router = APIRouter()


@router.post("", response_model=CustomerResponse)
async def create_customer(
    customer: CustomerCreate,
    db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    user_repo = UserRepository(db)

    # Check if email already exists
    if user_repo.get_by_email(customer.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_service = UserService(user_repo)
    customer_data = customer.dict()
    new_customer = user_service.register_customer(customer_data)

    return {k: v for k, v in new_customer.items() if k != "hashed_password"}


@router.get("", response_model=list[CustomerResponse])
async def get_customers_list(
    current_user: dict = Depends(get_current_customer),  # type: ignore # noqa: ARG001
    db: dict = Depends(get_db),
):
    user_repo = UserRepository(db)
    customers = user_repo.get_all_customers()
    return [{k: v for k, v in customer.items() if k != "hashed_password"} for customer in customers]


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(
    customer_id: str,
    current_user: dict = Depends(get_current_customer),  # type: ignore # noqa: ARG001
    db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    user_repo = UserRepository(db)
    customer = user_repo.get_by_id(customer_id, "customer")

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {k: v for k, v in customer.items() if k != "hashed_password"}


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
    current_user: dict = Depends(get_current_customer),  # type: ignore # noqa: ARG001
    db: dict = Depends(get_db),
):
    booking_repo = BookingRepository(db)
    customer_bookings = booking_repo.get_by_customer(current_user["id"])
    completed = [b for b in customer_bookings if b["status"] == "completed"]

    return StatsResponse(
        total_bookings=len(customer_bookings),
        completed_sessions=len(completed),
        active_membership=None,
        visit_count=current_user.get("visit_count", 0),
    )
