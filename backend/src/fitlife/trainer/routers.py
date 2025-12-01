from uuid import UUID

from fastapi import APIRouter
from starlette import status

from fitlife.database import SessionDep, get_all_entities, get_entity_by_uuid
from fitlife.schemas import BadResponse, OkResponse
from fitlife.trainer.models import TrainerModel
from fitlife.trainer.schemas import TrainersAddSchema, TrainersSchema

router = APIRouter()

title = '🏋️ Trainers'


@router.post(
    '/trainers',
    summary='Add new trainer',
    status_code=status.HTTP_201_CREATED,
    tags=[title],
    description='Add new trainer to the database',
    response_model=OkResponse,
)
async def add_trainer(trainer: TrainersAddSchema, session: SessionDep):
    new_trainer = TrainerModel(
        name=trainer.name,
        speciality=trainer.speciality,
    )
    session.add(new_trainer)
    await session.commit()
    return OkResponse(msg='Trainer successfully added!')


@router.get(
    '/trainers',
    summary='Get all trainers',
    tags=[title],
    description='Get all trainers from the database',
    response_model=list[TrainersSchema],
)
async def get_trainers(session: SessionDep):
    result = await get_all_entities(TrainerModel, session)
    return result


@router.get(
    '/trainers/{trainer_uuid}',
    summary='Get specific trainer by index',
    tags=[title],
    description='Get specific trainer from the database',
    response_model=TrainersSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Trainer not found',
        }
    },
)
async def get_specific_trainer(trainer_uuid: UUID, session: SessionDep):
    result = await get_entity_by_uuid(TrainerModel, trainer_uuid, session, 'Trainer not found!')
    return result
