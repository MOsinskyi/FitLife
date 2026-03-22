from fitlife.repositories import BaseUserRepository

from .models import MemberModel


class MemberRepository(BaseUserRepository[MemberModel]):
    model = MemberModel
