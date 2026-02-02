from fastapi import BackgroundTasks

from fitlife.coach.repositories import CoachRepository
from fitlife.config import settings
from fitlife.services import UserService


class CoachService(UserService):
    def __init__(self, repository: CoachRepository, background_tasks: BackgroundTasks):
        super().__init__(repository, background_tasks, settings.cache.namespace.coach)
