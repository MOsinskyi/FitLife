from fastapi import BackgroundTasks

from fitlife.config import settings
from fitlife.member.repositories import MemberRepository
from fitlife.services import UserService


class MemberService(UserService):
    def __init__(self, repository: MemberRepository, background_tasks: BackgroundTasks):
        super().__init__(repository, background_tasks, settings.cache.namespace.member)
