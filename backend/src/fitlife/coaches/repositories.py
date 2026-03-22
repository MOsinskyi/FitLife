from fitlife.repositories import BaseUserRepository

from .models import CoachModel
from .schemas import CoachUpdateSchema


class CoachRepository(BaseUserRepository[CoachModel]):
    model = CoachModel
    update_model_schema = CoachUpdateSchema
