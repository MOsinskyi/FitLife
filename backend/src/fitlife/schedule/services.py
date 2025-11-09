from datetime import datetime

from fastapi import HTTPException

from fitlife.schedule.repositories import ScheduleRepository


class ScheduleService:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo

    def create_schedule(self, schedule_data: dict, current_user_id: str):
        if schedule_data["coach_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Can only create schedules for yourself")

        # Validate time range
        start_time = schedule_data.get("start_time")
        end_time = schedule_data.get("end_time")

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        if start_time and end_time and end_time <= start_time:
            raise HTTPException(status_code=400, detail="End time must be after start time")

        return self.schedule_repo.create(schedule_data)

    def get_all_schedules(self):
        return self.schedule_repo.get_all()
