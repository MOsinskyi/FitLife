from fitlife.schedule.repositories import ScheduleRepository
from fastapi import HTTPException


class ScheduleService:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo

    def create_schedule(self, schedule_data: dict, current_user_id: str):
        if schedule_data["coach_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Can only create schedules for yourself")

        return self.schedule_repo.create(schedule_data)

    def get_all_schedules(self):
        return self.schedule_repo.get_all()
