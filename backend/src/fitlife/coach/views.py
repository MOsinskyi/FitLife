from fastapi import APIRouter, Depends, status
from typing import List
from fitlife.coach.schemas import CoachCreate, CoachResponse
from fitlife.customer.schemas import CustomerResponse
from fitlife.booking.schemas import VisitRecordResponse
from fitlife.deps import get_current_coach
from fitlife.database import get_db
from fitlife.user.repositories import UserRepository
from fitlife.user.services import UserService
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=CoachResponse, status_code=status.HTTP_201_CREATED)
async def register_coach(
        coach: CoachCreate,
        db: dict = Depends(get_db)
):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    coach_data = coach.model_dump()
    new_coach = user_service.register_coach(coach_data)

    return {k: v for k, v in new_coach.items() if k != "hashed_password"}

@router.post("/visits", response_model=VisitRecordResponse)
async def mark_customer_visit(
        customer_id: str,
        current_user: dict = Depends(get_current_coach),
        db: dict = Depends(get_db)
):
    user_repo = UserRepository(db)
    customer = user_repo.update_customer_visits(customer_id)

    if not customer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Customer not found")

    return VisitRecordResponse(
        id=str(uuid.uuid4()),
        customer_id=customer_id,
        visit_time=datetime.utcnow(),
        marked_by=current_user["id"]
    )

@router.get("/me/clients", response_model=List[CustomerResponse])
async def get_my_clients(
        current_user: dict = Depends(get_current_coach),
        db: dict = Depends(get_db)
):
    from fitlife.schedule.repositories import ScheduleRepository
    from fitlife.booking.repositories import BookingRepository

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