from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy import exists, select

from fitlife.database import SessionDep, add_entity, get_all_entities, get_entity_by_uuid
from fitlife.schemas import BadResponse, OkResponse
from fitlife.workout_session.models import WorkoutSessionModel
from fitlife.workout_session.schemas import WorkoutSessionAddSchema, WorkoutSessionSchema

router = APIRouter()

title = '🏋️ Workout Sessions'


@router.post(
    '/workout-sessions',
    status_code=status.HTTP_201_CREATED,
    summary='Create workout session',
    tags=[title],
    description='Add new workout session to the database',
    responses={
        status.HTTP_201_CREATED: {
            'model': OkResponse,
            'description': 'Workout session successfully created',
        },
        status.HTTP_409_CONFLICT: {
            'model': BadResponse,
            'description': 'Workout session already exists',
        },
    },
)
async def create_workout_session(workout_session: WorkoutSessionAddSchema, session: SessionDep):
    new_workout_session = WorkoutSessionModel(
        date=workout_session.date,
        time=workout_session.time,
    )

    date_exists = await session.scalar(select(exists().where(WorkoutSessionModel.date == workout_session.date)))
    time_exists = await session.scalar(select(exists().where(WorkoutSessionModel.time == workout_session.time)))

    await add_entity(new_workout_session, session, 'Workout session already exists', date_exists, time_exists)

    return OkResponse(msg='Workout session successfully created!')


@router.get(
    '/workout-sessions',
    summary='Show all workout sessions',
    tags=[title],
    description='Fetch all workout sessions from database',
    response_model=list[WorkoutSessionSchema],
)
async def get_workout_sessions(session: SessionDep):
    result = await get_all_entities(WorkoutSessionModel, session)
    return result


@router.get(
    '/workout-sessions/{workout_session_uuid}',
    summary='Show specific workout session',
    tags=[title],
    description='Fetch specific workout session from the database',
    response_model=WorkoutSessionSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': BadResponse,
            'description': 'Workout session not found',
        }
    },
)
async def get_specific_workout_session(workout_session_uuid: UUID, session: SessionDep):
    result = await get_entity_by_uuid(WorkoutSessionModel, workout_session_uuid, session, 'Workout session not found!')
    return result
