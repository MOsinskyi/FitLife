import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, status

from fitlife.booking.schemas import VisitRecordResponse
from fitlife.coach.schemas import CoachCreate, CoachResponse
from fitlife.customer.schemas import CustomerResponse
from fitlife.database import get_db
from fitlife.deps import get_current_coach
from fitlife.user.repositories import UserRepository
from fitlife.user.services import UserService

router = APIRouter()


@router.post("", response_model=CoachResponse)
async def create_coach(coach: CoachCreate, db: dict = Depends(get_db)):
    from fastapi import HTTPException

    user_repo = UserRepository(db)

    # Check if email already exists
    if user_repo.get_by_email(coach.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_service = UserService(user_repo)
    coach_data = coach.model_dump()
    new_coach = user_service.register_coach(coach_data)

    return {k: v for k, v in new_coach.items() if k != "hashed_password"}


@router.get("", response_model=list[CoachResponse])
async def get_coaches_list(
    current_user: dict = Depends(get_current_coach), db: dict = Depends(get_db)
):
    _ = current_user  # Required for authentication
    user_repo = UserRepository(db)
    coaches = user_repo.get_all_coaches()
    return [{k: v for k, v in coach.items() if k != "hashed_password"} for coach in coaches]


@router.get("/{coach_id}", response_model=CoachResponse)
async def get_coach_by_id(
    coach_id: str, current_user: dict = Depends(get_current_coach), db: dict = Depends(get_db)
):
    _ = current_user  # Required for authentication
    from fastapi import HTTPException

    user_repo = UserRepository(db)
    coach = user_repo.get_by_id(coach_id, "coach")

    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    return {k: v for k, v in coach.items() if k != "hashed_password"}


@router.post("/register", response_model=CoachResponse, status_code=status.HTTP_201_CREATED)
async def register_coach(coach: CoachCreate, db: dict = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    coach_data = coach.model_dump()
    new_coach = user_service.register_coach(coach_data)

    return {k: v for k, v in new_coach.items() if k != "hashed_password"}


@router.post("/visits", response_model=VisitRecordResponse)
async def mark_customer_visit(
    customer_id: str, current_user: dict = Depends(get_current_coach), db: dict = Depends(get_db)
):
    user_repo = UserRepository(db)
    customer = user_repo.update_customer_visits(customer_id)

    if not customer:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Customer not found")

    return VisitRecordResponse(
        id=str(uuid.uuid4()),
        customer_id=customer_id,
        visit_time=datetime.now(UTC),
        marked_by=current_user["id"],
    )


@router.get("/me/clients", response_model=list[CustomerResponse])
async def get_my_clients(
    current_user: dict = Depends(get_current_coach), db: dict = Depends(get_db)
):
    from fitlife.booking.repositories import BookingRepository
    from fitlife.schedule.repositories import ScheduleRepository

    schedule_repo = ScheduleRepository(db)
    booking_repo = BookingRepository(db)
    user_repo = UserRepository(db)

    coach_schedules = schedule_repo.get_by_coach(current_user["id"])
    coach_schedule_ids = [s["id"] for s in coach_schedules]

    client_ids = set()
    for schedule_id in coach_schedule_ids:
        bookings = booking_repo.get_by_schedule(schedule_id)
        for booking in bookings:
            client_ids.add(booking["customer_id"])

    clients = []
    for cid in client_ids:
        customer = user_repo.get_by_id(cid, "customer")
        if customer:
            clients.append({k: v for k, v in customer.items() if k != "hashed_password"})

    return clients
