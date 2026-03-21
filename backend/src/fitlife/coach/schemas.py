from collections.abc import Callable

from pydantic import Field

from fitlife.schemas import UserCredentialsSchema, UserRegisterSchema, UserRegisterWithRoleSchema, UserSchema

SPECIALITIES = ['Силові тренування', 'Функціональний фітнес', 'Йога та стретчинг', 'Кардіо та HIIT', 'Медитація']


class CoachCredentialsSchema(UserCredentialsSchema):
    speciality: str = Field(default=SPECIALITIES[0], title='Спеціальність', examples=SPECIALITIES)
    emoji_char: str = Field(default='🏋️‍', title='Emoji')
    experience: int = Field(default=1, title='Досвід', ge=1)
    experience_title: str = Field(default='рік')

    def validate_speciality(self, value: str, handle: Callable):  # noqa
        assert value not in SPECIALITIES, f'Invalid speciality, Valid specialities: {SPECIALITIES}'

        result = handle(value)

        return result


class CoachRegisterWithRoleSchema(UserRegisterWithRoleSchema, CoachCredentialsSchema):
    pass


class CoachRegisterSchema(UserRegisterSchema, CoachCredentialsSchema):
    pass


class CoachSchema(UserSchema, CoachCredentialsSchema):
    session_count: int = Field(default=0)
