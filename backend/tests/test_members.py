from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from fitlife.schemas import UserRegisterSchema, UserUpdateSchema
from fitlife.members.services import MemberService
from fitlife.security import Security

SECURITY = Security()


def get_mock_background_tasks():
    """Create a mock BackgroundTasks instance"""
    mock_bg = MagicMock()
    mock_bg.add_task = MagicMock()
    return mock_bg


class TestMemberRegistration:
    @pytest.mark.asyncio
    async def test_register_member_success(self):
        repo = MagicMock()
        repo.get_user_by_phone = AsyncMock(return_value=None)
        repo.get_user_by_email = AsyncMock(return_value=None)

        created_member = MagicMock()
        created_member.id = uuid4()
        created_member.role = 'member'
        created_member.password = ''
        repo.create_user = AsyncMock(return_value=created_member)

        security = MagicMock()
        security.hash_password = MagicMock(return_value='hashed_password')

        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )

        schema = UserRegisterSchema(
            first_name='Олена',
            last_name='Коваленко',
            email='olena@gym.ua',
            phone_number='+380671234567',
            password='password123',
        )

        result = await service.register_member(schema)

        repo.create_user.assert_awaited_once()
        security.hash_password.assert_called_once_with('password123')
        assert result.role == 'member'

    @pytest.mark.asyncio
    async def test_register_duplicate_email_raises_exception(self):
        from fitlife.exceptions import UserAlreadyExists

        existing_member = MagicMock()
        existing_member.email = 'duplicate@gym.ua'

        repo = MagicMock()
        repo.get_user_by_email = AsyncMock(return_value=existing_member)
        repo.get_user_by_phone = AsyncMock(return_value=None)

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )

        schema = UserRegisterSchema(
            first_name='Test',
            last_name='Member',
            email='duplicate@gym.ua',
            phone_number='+380671234567',
            password='password123',
        )

        with pytest.raises(UserAlreadyExists):
            await service.register_member(schema)

    @pytest.mark.asyncio
    async def test_register_duplicate_phone_raises_exception(self):
        from fitlife.exceptions import UserAlreadyExists

        existing_member = MagicMock()
        existing_member.phone_number = '+380671234567'

        repo = MagicMock()
        repo.get_user_by_phone = AsyncMock(return_value=existing_member)
        repo.get_user_by_email = AsyncMock(return_value=None)

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )

        schema = UserRegisterSchema(
            first_name='Test',
            last_name='Member',
            email='test@gym.ua',
            phone_number='+380671234567',
            password='password123',
        )

        with pytest.raises(UserAlreadyExists):
            await service.register_member(schema)


class TestMemberCRUD:
    @pytest.mark.asyncio
    async def test_get_all_members(self):
        member1 = MagicMock()
        member1.id = uuid4()
        member1.first_name = 'Іван'

        member2 = MagicMock()
        member2.id = uuid4()
        member2.first_name = 'Марія'

        repo = MagicMock()
        repo.get_users = AsyncMock(return_value=[member1, member2])

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )
        result = await service.get_all_members()

        assert isinstance(result, list)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_member_by_id_success(self):
        member_id = uuid4()
        mock_member = MagicMock()
        mock_member.id = member_id

        repo = MagicMock()
        repo.get_user_by_id = AsyncMock(return_value=mock_member)

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )
        result = await service.get_member_profile(member_id)

        assert result == mock_member

    @pytest.mark.asyncio
    async def test_get_member_by_id_not_found_raises_error(self):
        repo = MagicMock()
        repo.get_user_by_id = AsyncMock(return_value=None)

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )

        with pytest.raises(ValueError) as exc_info:
            await service.get_member_profile(uuid4())

        assert 'Member not found' in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_member_success(self):
        member_id = uuid4()
        mock_member = MagicMock()
        mock_member.id = member_id

        repo = MagicMock()
        repo.update_user = AsyncMock(return_value=mock_member)

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )

        schema = UserUpdateSchema(
            first_name='Нове ім\'я',
            last_name='Нове прізвище',
        )

        result = await service.update_member_profile(member_id, schema)

        repo.update_user.assert_awaited_once()
        assert result == mock_member

    @pytest.mark.asyncio
    async def test_delete_member_success(self):
        member_id = uuid4()
        mock_member = MagicMock()
        mock_member.id = member_id

        repo = MagicMock()
        repo.get_user_by_id = AsyncMock(return_value=mock_member)
        repo.delete_user = AsyncMock(return_value=None)

        security = MagicMock()
        service = MemberService(
            repository=repo,
            security=security,
            background_tasks=get_mock_background_tasks(),
            cache_namespace='test_member',
        )

        await service.delete_member_profile(member_id)

        repo.delete_user.assert_awaited_once_with(member_id)


class TestMemberSchemas:
    def test_member_register_schema_valid(self):
        schema = UserRegisterSchema(
            first_name='Петро',
            last_name='Сидоренко',
            email='petro@gym.ua',
            phone_number='+380671234567',
            password='password123',
        )

        assert schema.first_name == 'Петро'
        assert schema.last_name == 'Сидоренко'
        assert schema.email == 'petro@gym.ua'

    def test_member_update_schema_partial_update(self):
        schema = UserUpdateSchema(first_name='Нове ім\'я')

        assert schema.first_name == 'Нове ім\'я'
        assert schema.last_name is None
        assert schema.email is None

    @pytest.mark.parametrize('phone', [
        '+380671234567',
        '+380501234567',
        '+380991234567',
    ])
    def test_member_register_valid_ukrainian_phones(self, phone):
        schema = UserRegisterSchema(
            first_name='Test',
            last_name='User',
            email='test@gym.ua',
            phone_number=phone,
            password='password123',
        )

        assert schema.phone_number == phone
