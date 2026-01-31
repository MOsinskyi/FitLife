from typing import Annotated

from fastapi import BackgroundTasks, Depends

from fitlife.database import SessionDep
from fitlife.member.repositories import MemberSqlAlchemyRepository
from fitlife.member.services import MemberService


async def get_member_service(session: SessionDep, background_tasks: BackgroundTasks) -> MemberService:
    """
    Ця функція повертає асинхронний екземпляр сервісу для користувача
    :param background_tasks: Фонові завдання
    :param session: Сесія бази даних
    :return: Сервіс користувача
    """
    return MemberService(MemberSqlAlchemyRepository(session), background_tasks)


MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]
