from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fitlife.coaches.schemas import CoachRegisterSchema, CoachUpdateSchema, Specializations
from fitlife.coaches.services import CoachService
from fitlife.security import Security

SECURITY = Security()


def get_mock_background_tasks():
    """Create a mock BackgroundTasks instance"""
    mock_bg = MagicMock()
    mock_bg.add_task = MagicMock()
    return mock_bg


class TestCoachRegistration:
    @pytest.mark.asyncio
    async def test_register_coach_success(self):
        repo = MagicMock()
        repo.get_user_by_phone = AsyncMock(return_value=None)
        repo.get_user_by_email = AsyncMock(return_value=None)

        created_coach = MagicMock()
        created_coach.id = uuid4()
        created_coach.role = 'coach'
        created_coach.password = ''
        repo.create_user = AsyncMock(return_value=created_coach)

        security = MagicMock()
        security.hash_password = MagicMock(return_value='hashed_password')

        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )

        schema = CoachRegisterSchema(
            first_name='Тарас',
            last_name='Петренко',
            email='taras@gym.ua',
            phone_number='+380671234567',
            password='password123',
            specialization=Specializations.YOGA,
            experience=5,
        )

        result = await service.register_coach(schema)

        repo.create_user.assert_awaited_once()
        security.hash_password.assert_called_once_with('password123')
        assert result.role == 'coach'

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises_exception(self):
        from fitlife.exceptions import UserAlreadyExists

        existing_coach = MagicMock()
        existing_coach.email = 'duplicate@gym.ua'

        repo = MagicMock()
        repo.get_user_by_email = AsyncMock(return_value=existing_coach)
        repo.get_user_by_phone = AsyncMock(return_value=None)

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )

        schema = CoachRegisterSchema(
            first_name='Test',
            last_name='Coach',
            email='duplicate@gym.ua',
            phone_number='+380671234567',
            password='password123',
            specialization=Specializations.YOGA,
            experience=5,
        )

        with pytest.raises(UserAlreadyExists):
            await service.register_coach(schema)

    @pytest.mark.asyncio
    async def test_register_duplicate_phone_raises_exception(self):
        from fitlife.exceptions import UserAlreadyExists

        existing_coach = MagicMock()
        existing_coach.phone_number = '+380671234567'

        repo = MagicMock()
        repo.get_user_by_phone = AsyncMock(return_value=existing_coach)
        repo.get_user_by_email = AsyncMock(return_value=None)

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )

        schema = CoachRegisterSchema(
            first_name='Test',
            last_name='Coach',
            email='test@gym.ua',
            phone_number='+380671234567',
            password='password123',
            specialization=Specializations.YOGA,
            experience=5,
        )

        with pytest.raises(UserAlreadyExists):
            await service.register_coach(schema)


class TestCoachCRUD:
    @pytest.mark.asyncio
    async def test_get_all_coaches(self):
        coach1 = MagicMock()
        coach1.id = uuid4()
        coach1.first_name = 'Ivan'

        coach2 = MagicMock()
        coach2.id = uuid4()
        coach2.first_name = 'Olha'

        repo = MagicMock()
        repo.get_users = AsyncMock(return_value=[coach1, coach2])

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )
        result = await service.get_all_coaches()

        assert isinstance(result, list)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_coach_by_id_success(self):
        coach_id = uuid4()
        mock_coach = MagicMock()
        mock_coach.id = coach_id

        repo = MagicMock()
        repo.get_user_by_id = AsyncMock(return_value=mock_coach)

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )
        result = await service.get_coach_profile(coach_id)

        assert result == mock_coach

    @pytest.mark.asyncio
    async def test_get_coach_by_id_not_found_raises_error(self):
        repo = MagicMock()
        repo.get_user_by_id = AsyncMock(return_value=None)

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )

        with pytest.raises(ValueError) as exc_info:
            await service.get_coach_profile(uuid4())

        assert 'Coach not found' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_coach_success(self):
        coach_id = uuid4()
        mock_coach = MagicMock()
        mock_coach.id = coach_id

        repo = MagicMock()
        repo.update_user = AsyncMock(return_value=mock_coach)

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )

        schema = CoachUpdateSchema(
            specialization=Specializations.CROSSFIT,
            experience=10,
        )

        result = await service.update_coach_profile(coach_id, schema)

        repo.update_user.assert_awaited_once()
        assert result == mock_coach

    @pytest.mark.asyncio
    async def test_delete_coach_success(self):
        coach_id = uuid4()
        mock_coach = MagicMock()
        mock_coach.id = coach_id

        repo = MagicMock()
        repo.get_user_by_id = AsyncMock(return_value=mock_coach)
        repo.delete_user = AsyncMock(return_value=None)

        security = MagicMock()
        service = CoachService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_coach',
        )

        await service.delete_coach(coach_id)

        repo.delete_user.assert_awaited_once_with(coach_id)


class TestCoachSchemas:
    def test_coach_register_schema_valid(self):
        schema = CoachRegisterSchema(
            first_name='Тарас',
            last_name='Шевченко',
            email='taras@gym.ua',
            phone_number='+380671234567',
            password='password123',
            specialization=Specializations.YOGA,
            experience=8,
        )

        assert schema.first_name == 'Тарас'
        # Schema uses enum values (strings) not enum objects due to use_enum_values=True
        assert schema.specialization == Specializations.YOGA.value
        assert schema.experience == 8

    @pytest.mark.parametrize('experience', [-1, -5, 0])
    def test_coach_register_negative_experience_invalid(self, experience):
        import pydantic

        with pytest.raises(pydantic.ValidationError):
            CoachRegisterSchema(
                first_name='Test',
                last_name='Coach',
                email='test@gym.ua',
                phone_number='+380671234567',
                password='password123',
                specialization=Specializations.YOGA,
                experience=experience,
            )

    def test_coach_update_schema_partial_update(self):
        schema = CoachUpdateSchema(specialization=Specializations.YOGA)

        assert schema.specialization == Specializations.YOGA
        assert schema.experience is None
