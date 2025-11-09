import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, status

from fitlife.coach.schemas import CoachResponse
from fitlife.customer.schemas import CustomerResponse
from fitlife.database import get_db
from fitlife.deps import get_current_manager
from fitlife.membership.schemas import MembershipTypeCreate, MembershipTypeResponse
from fitlife.schedule.repositories import ScheduleRepository
from fitlife.schedule.schemas import ScheduleResponse
from fitlife.security import get_password_hash
from fitlife.user.repositories import UserRepository
from fitlife.user.schemas import UserCreate, UserResponse

router = APIRouter()


@router.post("", response_model=UserResponse)
async def create_manager(
        user: UserCreate,
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    user_repo = UserRepository(db)
    if user_repo.get_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)

    user_data = {
        "id": user_id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "role": "manager",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "hashed_password": hashed_password
    }

    db["accounts"][user.email] = user_data

    return {k: v for k, v in user_data.items() if k != "hashed_password"}


@router.get("", response_model=List[UserResponse])
async def get_managers_list(
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    user_repo = UserRepository(db)
    managers = user_repo.get_all_managers()
    return [{k: v for k, v in manager.items() if k != "hashed_password"} for manager in managers]


@router.get("/{manager_id}", response_model=UserResponse)
async def get_manager_by_id(
        manager_id: str,
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    user_repo = UserRepository(db)
    manager = user_repo.get_by_id(manager_id, "manager")

    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    return {k: v for k, v in manager.items() if k != "hashed_password"}


@router.post("/accounts", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
        user: UserCreate,
        role: str,
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    user_repo = UserRepository(db)
    if user_repo.get_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if role not in ["coach", "customer", "manager"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)

    user_data = {
        "id": user_id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "role": role,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "hashed_password": hashed_password
    }

    db["accounts"][user.email] = user_data

    return {k: v for k, v in user_data.items() if k != "hashed_password"}


@router.get("/coaches", response_model=List[CoachResponse])
async def get_all_coaches(
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    user_repo = UserRepository(db)
    coaches = user_repo.get_all_coaches()
    return [{k: v for k, v in coach.items() if k != "hashed_password"} for coach in coaches]


@router.get("/customers", response_model=List[CustomerResponse])
async def get_all_customers(
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    user_repo = UserRepository(db)
    customers = user_repo.get_all_customers()
    return [{k: v for k, v in customer.items() if k != "hashed_password"} for customer in customers]


@router.get("/schedules", response_model=List[ScheduleResponse])
async def control_schedules(
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    schedule_repo = ScheduleRepository(db)
    return schedule_repo.get_all()


@router.delete("/schedules/{schedule_id}")
async def delete_schedule(
        schedule_id: str,
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    from fastapi import HTTPException
    schedule_repo = ScheduleRepository(db)

    if not schedule_repo.delete(schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")

    return {"message": "Schedule deleted successfully"}


@router.post("/membership-types", response_model=MembershipTypeResponse)
async def create_membership_type(
        membership: MembershipTypeCreate,
        current_user: dict = Depends(get_current_manager),
        db: dict = Depends(get_db),
):
    membership_id = str(uuid.uuid4())
    membership_data = {
        "id": membership_id,
        **membership.dict()
    }

    db["memberships"][membership_id] = membership_data
    return membership_data
