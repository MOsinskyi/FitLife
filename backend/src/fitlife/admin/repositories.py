from fitlife.repositories import BaseUserRepository
from .models import AdminModel


class AdminRepository(BaseUserRepository[AdminModel]):
    model = AdminModel
