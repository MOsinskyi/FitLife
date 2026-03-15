from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TrainingSessionAddSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    title: str = Field(
        title='Заголовок',
        description='Заголовок для сесії.',
        examples=[
            'Заняття з йоги.',
        ],
    )
    description: str = Field(
        title='Опис',
        description='Опис для сесії.',
        examples=['Відвідайте наші ранкові заняття з йоги, які дадуть вам сил на цілий день.'],
    )
    max_participants: int = Field(
        default=4,
        title='Кількість учасників',
        description='Максимальна кількість учасників для сесії.',
        ge=1,
        le=50,
    )
    price: int = Field(
        default=0,
        title='Ціна',
        description='Ціна за одне заняття',
    )
    duration_minutes: int = Field(
        default=60,
        title='Тривалість',
        description='Тривалість одного заняття в хвилинах.',
        ge=15,
        le=180,
    )
    coach_id: UUID = Field(
        title='Ідентифікатор тренера',
        description='Ідентифікатор тренера, який проводить тренування.',
    )
    members_ids: list[UUID] = Field(
        default_factory=list,
        validation_alias='members',
        title='Ідентифікатори учасників',
        description='Список ідентифікаторів учасників сесії.',
    )

    @field_validator('members_ids', mode='before')
    @classmethod
    def extract_members_ids(cls, v: Any) -> list[UUID]:
        if not v:
            return []

        return [item.id if hasattr(item, 'id') else item for item in v]


class TrainingSessionSchema(TrainingSessionAddSchema):
    id: UUID = Field(
        default_factory=uuid4,
        title='Ідентифікатор',
        description='Унікальний ідентифікатор',
    )
