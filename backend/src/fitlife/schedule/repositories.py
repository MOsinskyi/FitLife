import uuid
from datetime import UTC, datetime
from typing import Any


class ScheduleRepository:
    def __init__(self, db: dict[str, Any]):
        self.schedules_db: dict[str, Any] = db["schedules"]

    def create(self, schedule_data: dict[str, Any]) -> dict[str, Any]:
        schedule_id = str(uuid.uuid4())
        schedule: dict[str, Any] = {
            "id": schedule_id,
            **schedule_data,
            "created_at": datetime.now(UTC),
            "participants_count": 0,
        }
        self.schedules_db[schedule_id] = schedule
        return schedule

    def get_by_id(self, schedule_id: str) -> dict[Any, Any] | None:
        result: dict[Any, Any] | None = self.schedules_db.get(schedule_id)
        return result

    def get_all(self) -> list[dict]:
        return list(self.schedules_db.values())

    def get_by_coach(self, coach_id: str) -> list[dict]:
        return [s for s in self.schedules_db.values() if s["coach_id"] == coach_id]

    def delete(self, schedule_id: str) -> bool:
        if schedule_id in self.schedules_db:
            del self.schedules_db[schedule_id]
            return True
        return False

    def increment_participants(self, schedule_id: str) -> dict[Any, Any] | None:
        schedule: dict[Any, Any] | None = self.schedules_db.get(schedule_id)
        if schedule:
            schedule["participants_count"] += 1
            return schedule
        return None
