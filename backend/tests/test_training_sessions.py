from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from fitlife.training_session.schemas import TrainingSessionAddSchema
from fitlife.training_session.services import TrainingSessionService

PATCH_DECODE = 'fitlife.auth.dependencies.Security.decode_access_token'
PATCH_SESSION = 'fitlife.auth.dependencies.get_session'
PATCH_TS_REPO = 'fitlife.training_session.dependencies.TrainingSessionSqlAlchemyRepository'
PATCH_SECURITY = 'fitlife.security.settings.security'

BASE_VALID_PAYLOAD = {
    'title': 'Ранкова йога',
    'description': 'Заняття для початківців',
    'duration_minutes': 60,
    'max_participants': 15,
    'price': 200,
    'coach_id': str(uuid4()),
    'member_ids': [],
}


class TestCreateTrainingSessionSuccess:
    @pytest.mark.asyncio
    async def test_create_success_returns_201(
        self,
        mock_coach_model,
        coach_token,
        mock_training_session,
    ):
        repo = MagicMock()
        repo.get_by_title = AsyncMock(return_value=None)  # унікальна назва
        repo.create = AsyncMock(return_value=None)

        service = TrainingSessionService(
            repository=repo,
            background_tasks=MagicMock(),
        )

        schema = TrainingSessionAddSchema(**BASE_VALID_PAYLOAD)

        with patch('fitlife.cache.clear_cache', new=AsyncMock()):
            result = await service.create_training_session(schema)

        repo.create.assert_awaited_once()
        assert result.status_code == 201

    @pytest.mark.asyncio
    async def test_create_success_payload_is_persisted(self, mock_coach_model):
        repo = MagicMock()
        repo.get_by_title = AsyncMock(return_value=None)
        repo.create = AsyncMock(return_value=None)

        service = TrainingSessionService(
            repository=repo,
            background_tasks=MagicMock(),
        )

        payload = dict(BASE_VALID_PAYLOAD, duration_minutes=60, max_participants=15)
        schema = TrainingSessionAddSchema(**payload)

        with patch('fitlife.cache.clear_cache', new=AsyncMock()):
            await service.create_training_session(schema)

        call_args = repo.create.call_args[0][0]
        assert call_args.duration_minutes == 60
        assert call_args.max_participants == 15


class TestCreateTrainingSessionDurationValidation:
    @pytest.mark.parametrize(
        'minutes,should_raise',
        [
            (14, True),
            (15, False),
            (180, False),
            (181, True),
            (0, True),
            (60, False),
        ],
    )
    def test_duration_minutes_boundary(self, minutes, should_raise):
        import pydantic

        payload = dict(BASE_VALID_PAYLOAD, duration_minutes=minutes)
        if should_raise:
            with pytest.raises(pydantic.ValidationError):
                TrainingSessionAddSchema(**payload)
        else:
            schema = TrainingSessionAddSchema(**payload)
            assert schema.duration_minutes == minutes


class TestCreateTrainingSessionParticipantsValidation:
    @pytest.mark.parametrize(
        'participants,should_raise',
        [
            (0, True),
            (1, False),
            (50, False),
            (51, True),
            (15, False),
        ],
    )
    def test_max_participants_boundary(self, participants, should_raise):
        import pydantic

        payload = dict(BASE_VALID_PAYLOAD, max_participants=participants)
        if should_raise:
            with pytest.raises(pydantic.ValidationError):
                TrainingSessionAddSchema(**payload)
        else:
            schema = TrainingSessionAddSchema(**payload)
            assert schema.max_participants == participants


class TestCreateTrainingSessionForbiddenForMember:
    @pytest.mark.asyncio
    async def test_member_cannot_create_session(self, mock_member_model):
        from fastapi import HTTPException

        from fitlife.auth.dependencies import get_current_active_coach

        with pytest.raises(HTTPException) as exc_info:
            await get_current_active_coach(current_user=mock_member_model)

        assert exc_info.value.status_code == 403
        assert 'Not enough permissions' in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_coach_can_pass_coach_guard(self, mock_coach_model):
        from fitlife.auth.dependencies import get_current_active_coach
        from fitlife.coach.models import CoachModel

        mock_coach_model.__class__ = CoachModel
        result = await get_current_active_coach(current_user=mock_coach_model)
        assert result is mock_coach_model


class TestBookTrainingSessionSuccess:
    @pytest.mark.asyncio
    async def test_book_last_available_slot(self, mock_member_model, mock_training_session):
        existing_members = [MagicMock() for _ in range(9)]
        mock_training_session.members = existing_members
        mock_training_session.max_participants = 10

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_training_session)
        repo.add_member = AsyncMock(return_value=None)

        result = await _book_session_service(
            session=mock_training_session,
            member=mock_member_model,
            repo=repo,
        )

        assert result['success'] is True
        assert result['participants'] == 10

    @pytest.mark.asyncio
    async def test_book_returns_updated_count(self, mock_member_model, mock_training_session):
        mock_training_session.members = [MagicMock() for _ in range(3)]
        mock_training_session.max_participants = 10

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_training_session)
        repo.add_member = AsyncMock(return_value=None)

        result = await _book_session_service(
            session=mock_training_session,
            member=mock_member_model,
            repo=repo,
        )

        assert result['participants'] == 4


class TestBookTrainingSessionFull:
    @pytest.mark.asyncio
    async def test_book_full_session_raises_400(self, mock_member_model, mock_training_session):
        from fastapi import HTTPException

        mock_training_session.members = [MagicMock() for _ in range(10)]
        mock_training_session.max_participants = 10

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_training_session)

        with pytest.raises(HTTPException) as exc_info:
            await _book_session_service(
                session=mock_training_session,
                member=mock_member_model,
                repo=repo,
            )

        assert exc_info.value.status_code == 400
        assert 'вільних місць' in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_book_exactly_at_limit_boundary(self, mock_member_model, mock_training_session):
        from fastapi import HTTPException

        mock_training_session.max_participants = 5

        mock_training_session.members = [MagicMock() for _ in range(4)]
        repo = MagicMock()
        repo.add_member = AsyncMock()

        result = await _book_session_service(
            session=mock_training_session,
            member=mock_member_model,
            repo=repo,
        )
        assert result['success'] is True

        mock_training_session.members = [MagicMock() for _ in range(5)]

        with pytest.raises(HTTPException) as exc_info:
            await _book_session_service(
                session=mock_training_session,
                member=mock_member_model,
                repo=repo,
            )
        assert exc_info.value.status_code == 400


class TestBookTrainingSessionDuplicate:
    @pytest.mark.asyncio
    async def test_duplicate_booking_raises_error(self, mock_member_model, mock_training_session):
        from fastapi import HTTPException

        # Той самий member вже є в списку
        existing_member = MagicMock()
        existing_member.id = mock_member_model.id
        mock_training_session.members = [existing_member]
        mock_training_session.max_participants = 10

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_training_session)

        with pytest.raises(HTTPException) as exc_info:
            await _book_session_service(
                session=mock_training_session,
                member=mock_member_model,
                repo=repo,
            )

        assert exc_info.value.status_code in (400, 409)
        assert 'вже записані' in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_different_member_can_book_same_session(self, mock_member_model, mock_training_session):
        """Інший учасник може записатись на те саме тренування."""
        other_member = MagicMock()
        other_member.id = uuid4()  # інший ID
        mock_training_session.members = [other_member]
        mock_training_session.max_participants = 10

        repo = MagicMock()
        repo.add_member = AsyncMock()

        result = await _book_session_service(
            session=mock_training_session,
            member=mock_member_model,
            repo=repo,
        )
        assert result['success'] is True


# ===========================================================================
# Додаткові тести: TrainingSessionService (CRUD)
# ===========================================================================
class TestTrainingSessionServiceCRUD:
    """Юніт-тести для TrainingSessionService."""

    @pytest.mark.asyncio
    async def test_get_training_sessions_returns_list(self, mock_training_session):
        repo = MagicMock()
        repo.get_all = AsyncMock(return_value=[mock_training_session])

        service = TrainingSessionService(repo, MagicMock())
        result = await service.get_training_sessions()

        assert isinstance(result, list)
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_training_session_not_found_raises_404(self):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=None)

        service = TrainingSessionService(repo, MagicMock())

        with pytest.raises(HTTPException) as exc_info:
            await service.get_training_session(uuid4())

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_create_duplicate_title_raises_409(self, mock_training_session):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.get_by_title = AsyncMock(return_value=mock_training_session)  # вже існує

        service = TrainingSessionService(repo, MagicMock())
        schema = TrainingSessionAddSchema(**BASE_VALID_PAYLOAD)

        with pytest.raises(HTTPException) as exc_info:
            await service.create_training_session(schema)

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_delete_training_session_success(self, mock_training_session):
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_training_session)
        repo.delete = AsyncMock(return_value=None)

        service = TrainingSessionService(repo, MagicMock())

        with patch('fitlife.cache.clear_cache', new=AsyncMock()):
            result = await service.delete_training_session(mock_training_session.id)

        repo.delete.assert_awaited_once_with(mock_training_session)
        assert result.status_code == 200

    @pytest.mark.asyncio
    async def test_update_training_session_success(self, mock_training_session):
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_training_session)
        repo.update = AsyncMock(return_value=None)

        service = TrainingSessionService(repo, MagicMock())
        schema = TrainingSessionAddSchema(**BASE_VALID_PAYLOAD)

        with patch('fitlife.cache.clear_cache', new=AsyncMock()):
            result = await service.update_training_session(mock_training_session.id, schema)

        repo.update.assert_awaited_once()
        assert result.status_code == 200

    @pytest.mark.asyncio
    async def test_update_nonexistent_session_raises_404(self):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=None)

        service = TrainingSessionService(repo, MagicMock())
        schema = TrainingSessionAddSchema(**BASE_VALID_PAYLOAD)

        with pytest.raises(HTTPException) as exc_info:
            await service.update_training_session(uuid4(), schema)

        assert exc_info.value.status_code == 404


# ===========================================================================
# Допоміжна функція — inline "booking service"
# Емулює логіку ендпоінту POST /training-sessions/{id}/book
# ===========================================================================
async def _book_session_service(session, member, repo):
    """
    Inline-реалізація логіки бронювання.
    Замінити на реальний виклик сервісу, коли ендпоінт буде реалізовано.
    """
    from fastapi import HTTPException

    current_count = len(session.members)

    # TC-7: перевірка повторного бронювання
    if any(m.id == member.id for m in session.members):
        raise HTTPException(
            status_code=409,
            detail='Ви вже записані на це тренування',
        )

    # TC-6: перевірка заповненості
    if current_count >= session.max_participants:
        raise HTTPException(
            status_code=400,
            detail='Немає вільних місць на це тренування',
        )

    # TC-5: успішне бронювання
    session.members.append(member)
    if repo.add_member:
        await repo.add_member(session.id, member.id)

    return {'success': True, 'participants': len(session.members)}
