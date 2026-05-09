import enum
from typing import Annotated

from pydantic import ConfigDict, Field

from fitlife import schemas as base


class Specializations(enum.Enum):
    YOGA = 'Yoga'
    CROSSFIT = 'CrossFit'
    AEROBICS = 'Aerobics'
    STRENGTH_TRAINING = 'Strength Training'
    CARDIO = 'Cardio'
    MEDITATION = 'Meditation'


class Emojis(enum.Enum):
    YOGA = '🧘'
    CROSSFIT = '🏋️'
    AEROBICS = '🤸'
    STRENGTH_TRAINING = '💪'
    CARDIO = '🏃'
    MEDITATION = '🪷'


class CoachCreateSchema(base.UserCreateSchema):
    specializations: Annotated[list[Specializations], Field(default_factory=lambda: [Specializations.STRENGTH_TRAINING])]
    emoji: Annotated[Emojis, Field(default=Emojis.STRENGTH_TRAINING)]
    experience: Annotated[int, Field(default=1, ge=1)]
    experience_label: Annotated[str, Field(default='рік')]

    model_config = ConfigDict(use_enum_values=True)


class CoachRegisterSchema(base.UserRegisterSchema, CoachCreateSchema):
    pass


class CoachUpdateSchema(base.UserUpdateSchema):
    specializations: list[Specializations] | None = None
    emoji: Emojis | None = None
    experience: int | None = None
    experience_label: str | None = None


class CoachSchema(base.UserSchema, CoachCreateSchema):
    role: str = 'coach'
