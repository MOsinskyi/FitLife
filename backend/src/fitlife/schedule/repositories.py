import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List


class ScheduleRepository:
    def __init__(self, db: dict):
        self.schedules_db = db["schedules"]

    def create(self, schedule_data: dict) -> Dict:
        schedule_id = str(uuid.uuid4())
        schedule = {
            "id": schedule_id,
            **schedule_data,
            "created_at": datetime.now(timezone.utc),
            "participants_count": 0
        }
        self.schedules_db[schedule_id] = schedule
        return schedule

    def get_by_id(self, schedule_id: str) -> Optional[Dict]:
        return self.schedules_db.get(schedule_id)

    def get_all(self) -> List[Dict]:
        return list(self.schedules_db.values())

    def get_by_coach(self, coach_id: str) -> List[Dict]:
        return [s for s in self.schedules_db.values() if s["coach_id"] == coach_id]

    def delete(self, schedule_id: str) -> bool:
        if schedule_id in self.schedules_db:
            del self.schedules_db[schedule_id]
            return True
        return False

    def increment_participants(self, schedule_id: str) -> Optional[Dict]:
        schedule = self.schedules_db.get(schedule_id)
        if schedule:
            schedule["participants_count"] += 1
        return schedule
