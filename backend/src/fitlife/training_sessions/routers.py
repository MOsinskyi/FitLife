from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from fitlife.training_sessions.dependencies import TrainingSessionServiceDep
from fitlife.training_sessions.schemas import (
    TrainingSessionCreateSchema,
    TrainingSessionSchema,
    TrainingSessionUpdateSchema,
)

training_session_router = APIRouter(prefix='/training-sessions', tags=['🏋️ Training Sessions'])


@training_session_router.post(
    '/',
    response_model=TrainingSessionSchema,
    status_code=status.HTTP_201_CREATED,
    description='Create a new training session',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Training session created successfully',
            'model': TrainingSessionSchema,
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Invalid data or coach not found',
        },
    },
)
async def create_training_session(data: TrainingSessionCreateSchema, service: TrainingSessionServiceDep):
    try:
        return await service.create_training_session(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@training_session_router.get(
    '/',
    response_model=list[TrainingSessionSchema],
    description='Get all training sessions',
    responses={
        status.HTTP_200_OK: {
            'description': 'List of all training sessions',
            'model': list[TrainingSessionSchema],
        },
    },
)
async def get_all_training_sessions(service: TrainingSessionServiceDep):
    return await service.get_all_training_sessions()


@training_session_router.get(
    '/{session_id}',
    response_model=TrainingSessionSchema,
    description='Get training session by ID',
    responses={
        status.HTTP_200_OK: {
            'description': 'Training session details',
            'model': TrainingSessionSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Training session not found',
        },
    },
)
async def get_training_session(session_id: UUID, service: TrainingSessionServiceDep):
    try:
        return await service.get_training_session(session_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@training_session_router.put(
    '/{session_id}',
    response_model=TrainingSessionSchema,
    description='Update training session',
    responses={
        status.HTTP_200_OK: {
            'description': 'Training session updated successfully',
            'model': TrainingSessionSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Training session not found',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Invalid data',
        },
    },
)
async def update_training_session(
    session_id: UUID, data: TrainingSessionUpdateSchema, service: TrainingSessionServiceDep
):
    try:
        return await service.update_training_session(session_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@training_session_router.delete(
    '/{session_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Delete training session',
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'Training session deleted successfully',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Training session not found',
        },
    },
)
async def delete_training_session(session_id: UUID, service: TrainingSessionServiceDep):
    try:
        await service.delete_training_session(session_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@training_session_router.post(
    '/{session_id}/participants',
    response_model=TrainingSessionSchema,
    description='Add participants to training session',
    responses={
        status.HTTP_200_OK: {
            'description': 'Participants added successfully',
            'model': TrainingSessionSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Training session or member not found',
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Session is full or member already participating',
        },
    },
)
async def add_participants(session_id: UUID, member_ids: list[UUID], service: TrainingSessionServiceDep):
    try:
        return await service.add_participants_to_session(session_id, member_ids)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@training_session_router.delete(
    '/{session_id}/participants/{member_id}',
    response_model=TrainingSessionSchema,
    description='Remove participant from training session',
    responses={
        status.HTTP_200_OK: {
            'description': 'Participant removed successfully',
            'model': TrainingSessionSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Training session not found or member not participating',
        },
    },
)
async def remove_participant(session_id: UUID, member_id: UUID, service: TrainingSessionServiceDep):
    try:
        return await service.remove_participant_from_session(session_id, member_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@training_session_router.get(
    '/coach/{coach_id}',
    response_model=list[TrainingSessionSchema],
    description='Get all training sessions for a specific coach',
    responses={
        status.HTTP_200_OK: {
            'description': 'List of training sessions for the coach',
            'model': list[TrainingSessionSchema],
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Coach not found',
        },
    },
)
async def get_sessions_by_coach(coach_id: UUID, service: TrainingSessionServiceDep):
    try:
        return await service.get_sessions_by_coach(coach_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@training_session_router.get(
    '/member/{member_id}',
    response_model=list[TrainingSessionSchema],
    description='Get all training sessions for a specific member',
    responses={
        status.HTTP_200_OK: {
            'description': 'List of training sessions for the member',
            'model': list[TrainingSessionSchema],
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Member not found',
        },
    },
)
async def get_sessions_by_member(member_id: UUID, service: TrainingSessionServiceDep):
    try:
        return await service.get_sessions_by_member(member_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
