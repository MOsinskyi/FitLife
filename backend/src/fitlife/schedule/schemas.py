from datetime import datetime

from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    coach_id: str
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    max_participants: int = 10
    training_type: str | None = None


class ScheduleResponse(ScheduleCreate):
    id: str
    created_at: datetime
    participants_count: int = 0
