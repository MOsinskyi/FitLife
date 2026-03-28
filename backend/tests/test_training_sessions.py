from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fitlife.training_sessions.schemas import TrainingSessionCreateSchema
from fitlife.training_sessions.services import TrainingSessionService

BASE_VALID_PAYLOAD = {
    'title': 'Ранкова йога',
    'description': 'Заняття для початківців',
    'start_time': '09:00',
    'end_time': '10:00',
    'max_participants': 10,
    'coach': uuid4(),
    'participants': [],
}


class TestTrainingSessionService:
    @pytest.mark.asyncio
    async def test_create_training_session_success(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        mock_coach = MagicMock()
        mock_coach.id = BASE_VALID_PAYLOAD['coach']
        coach_repo.get_user_by_id = AsyncMock(return_value=mock_coach)

        created_session = MagicMock()
        created_session.id = uuid4()
        created_session.participants = []
        ts_repo.create_training_session = AsyncMock(return_value=created_session)
        ts_repo.get_training_session_by_id = AsyncMock(return_value=created_session)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        schema = TrainingSessionCreateSchema(**BASE_VALID_PAYLOAD)
        result = await service.create_training_session(schema)

        ts_repo.create_training_session.assert_awaited_once()
        assert result == created_session

    @pytest.mark.asyncio
    async def test_create_training_session_coach_not_found_raises_error(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        coach_repo.get_user_by_id = AsyncMock(return_value=None)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        schema = TrainingSessionCreateSchema(**BASE_VALID_PAYLOAD)

        with pytest.raises(ValueError) as exc_info:
            await service.create_training_session(schema)

        assert 'Coach' in str(exc_info.value)
        assert 'not found' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_training_session_success(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        session_id = uuid4()
        mock_session = MagicMock()
        mock_session.id = session_id

        ts_repo.get_training_session_by_id = AsyncMock(return_value=mock_session)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        result = await service.get_training_session(session_id)

        assert result == mock_session

    @pytest.mark.asyncio
    async def test_get_training_session_not_found_raises_error(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        ts_repo.get_training_session_by_id = AsyncMock(return_value=None)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        with pytest.raises(ValueError) as exc_info:
            await service.get_training_session(uuid4())

        assert 'Training session' in str(exc_info.value)
        assert 'not found' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_all_training_sessions(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        session1 = MagicMock()
        session2 = MagicMock()
        ts_repo.get_training_sessions = AsyncMock(return_value=[session1, session2])

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        result = await service.get_all_training_sessions()

        assert isinstance(result, list)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_delete_training_session_success(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        session_id = uuid4()
        mock_session = MagicMock()
        mock_session.id = session_id

        ts_repo.get_training_session_by_id = AsyncMock(return_value=mock_session)
        ts_repo.delete_training_session = AsyncMock(return_value=None)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        await service.delete_training_session(session_id)

        ts_repo.delete_training_session.assert_awaited_once_with(session_id)

    @pytest.mark.asyncio
    async def test_add_participants_to_session_success(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        session_id = uuid4()
        member_id = uuid4()

        mock_session = MagicMock()
        mock_session.id = session_id
        mock_session.participants = []
        mock_session.max_participants = 10

        mock_member = MagicMock()
        mock_member.id = member_id

        ts_repo.get_training_session_by_id = AsyncMock(return_value=mock_session)
        member_repo.get_user_by_id = AsyncMock(return_value=mock_member)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        result = await service.add_participants_to_session(session_id, [member_id])

        member_repo.get_user_by_id.assert_awaited_once_with(member_id)
        assert result == mock_session

    @pytest.mark.asyncio
    async def test_add_participants_exceeds_max_raises_error(self):
        ts_repo = MagicMock()
        coach_repo = MagicMock()
        member_repo = MagicMock()

        session_id = uuid4()
        member_id = uuid4()

        # Mock session that's already full
        mock_session = MagicMock()
        mock_session.id = session_id
        mock_session.participants = [MagicMock() for _ in range(10)]
        mock_session.max_participants = 10

        ts_repo.get_training_session_by_id = AsyncMock(return_value=mock_session)

        service = TrainingSessionService(
            training_session_repository=ts_repo,
            coach_repository=coach_repo,
            member_repository=member_repo,
        )

        with pytest.raises(ValueError) as exc_info:
            await service.add_participants_to_session(session_id, [member_id])

        assert 'Cannot add' in str(exc_info.value)


class TestTrainingSessionSchemas:
    @pytest.mark.parametrize(
        'participants,should_raise',
        [
            (0, True),
            (1, False),
            (12, False),
            (13, True),
            (10, False),
        ],
    )
    def test_max_participants_boundary(self, participants, should_raise):
        import pydantic

        payload = dict(BASE_VALID_PAYLOAD, max_participants=participants)
        if should_raise:
            with pytest.raises(pydantic.ValidationError):
                TrainingSessionCreateSchema(**payload)
        else:
            schema = TrainingSessionCreateSchema(**payload)
            assert schema.max_participants == participants
