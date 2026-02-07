from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TrainingSessionAddSchema(BaseModel):
    title: str = Field(
        title='Заголовок',
        description='Заголовок для сесії',
        examples=[
            'Заняття з йоги',
        ],
    )
    description: str = Field(
        title='Опис',
        description='Опис для сесії',
        examples=['Відвідайте наші ранкові заняття з йоги, які дадуть вам сил на цілий день'],
    )
    max_participants: int = Field(
        default=4,
        title='Кількість учасників',
        description='Максимальна кількість учасників для сесії',
    )
    price: int = Field(
        default=0,
        title='Ціна',
        description='Ціна за одне заняття',
    )
    duration_minutes: int = Field(
        default=60,
        title='Тривалість',
        description='Тривалість одного заняття в хвилинах',
    )


class TrainingSessionSchema(TrainingSessionAddSchema):
    id: UUID = Field(
        default_factory=uuid4,
        title='Ідентифікатор',
        description='Унікальний ідентифікатор',
    )
