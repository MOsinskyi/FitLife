from typing import TYPE_CHECKING

from fitlife.exceptions import InvalidCredentialsException

from .schemas import TokenSchema

if TYPE_CHECKING:
    from fitlife.coaches.repositories import CoachRepository
    from fitlife.members.repositories import MemberRepository
    from fitlife.security import Security


class AuthService:
    def __init__(
        self,
        member_repository: 'MemberRepository',
        coach_repository: 'CoachRepository',
        security: 'Security',
    ):
        self.member_repository = member_repository
        self.coach_repository = coach_repository
        self.security = security

    async def authenticate_user(self, phone_number: str, password: str) -> TokenSchema:
        user = await self.member_repository.get_user_by_phone(phone_number)

        if not user:
            user = await self.coach_repository.get_user_by_phone(phone_number)

        if not user:
            raise ValueError('User not found')

        if not self.security.verify_password(password, user.password):
            raise InvalidCredentialsException('Invalid password or phone number')

        access_token = self.security.create_access_token({'sub': str(user.id), 'role': user.role})

        return TokenSchema(access_token=access_token)
