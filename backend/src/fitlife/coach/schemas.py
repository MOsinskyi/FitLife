from collections.abc import Callable

from pydantic import Field

from fitlife.schemas import UserCredentialsSchema, UserRegisterSchema, UserSchema

SPECIALITIES = ['Силові тренування', 'Функціональний фітнес', 'Йога та стретчинг', 'Кардіо та HIIT', 'Медитація']


class CoachCredentialsSchema(UserCredentialsSchema):
    speciality: str = Field(default=SPECIALITIES[0], title='Спеціальність', examples=SPECIALITIES)
    emoji_entity: str = Field(default='&#x1F3CB;', title='Emoji', description='HTML entity (hex)')
    experience: int = Field(default=1, title='Досвід', ge=1)
    experience_title: str = Field(default='рік')

    def validate_speciality(self, value: str, handle: Callable):  # noqa: PLR6301
        assert value not in SPECIALITIES, f'Invalid speciality, Valid specialities: {SPECIALITIES}'

        result = handle(value)

        return result


class CoachRegisterSchema(UserRegisterSchema, CoachCredentialsSchema):
    pass


class CoachSchema(UserSchema, CoachCredentialsSchema):
    pass
