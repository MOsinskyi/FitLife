from typing import List

from fastapi import APIRouter, Depends, status

from fitlife.database import get_db
from fitlife.deps import get_current_coach, get_current_user
from fitlife.schedule.repositories import ScheduleRepository
from fitlife.schedule.schemas import ScheduleCreate, ScheduleResponse
from fitlife.schedule.services import ScheduleService

router = APIRouter()


@router.post("", response_model=ScheduleResponse)
async def create_schedule(
        schedule_data: ScheduleCreate,
        current_user: dict = Depends(get_current_coach),
        db: dict = Depends(get_db),
):
    schedule_repo = ScheduleRepository(db)
    schedule_service = ScheduleService(schedule_repo)

    schedule = schedule_service.create_schedule(schedule_data.dict(), current_user["id"])
    return schedule


@router.get("", response_model=List[ScheduleResponse])
async def view_schedules(
        current_user: dict = Depends(get_current_user),
        db: dict = Depends(get_db),
):
    schedule_repo = ScheduleRepository(db)
    return schedule_repo.get_all()


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule_by_id(
        schedule_id: str,
        current_user: dict = Depends(get_current_user),
        db: dict = Depends(get_db),
):
    from fastapi import HTTPException

    schedule_repo = ScheduleRepository(db)
    schedule = schedule_repo.get_by_id(schedule_id)

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return schedule
