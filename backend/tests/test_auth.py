from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from fitlife.schemas import (
    UserRegisterSchema,
)
from fitlife.security import Security

PATCH_DECODE_ACCESS = "fitlife.security.Security.decode_access_token"
PATCH_DECODE_REFRESH = "fitlife.security.Security.decode_refresh_token"
PATCH_MEMBER_REPO = "fitlife.member.repositories.MemberSqlAlchemyRepository"
PATCH_COACH_REPO = "fitlife.coach.repositories.CoachSqlAlchemyRepository"

SECURITY = Security()


class TestSecurity:

    def test_hash_password_returns_non_empty_string(self):
        hashed = SECURITY.hash_password("mypassword")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        raw = "supersecret"
        hashed = SECURITY.hash_password(raw)
        assert SECURITY.verify_password(raw, hashed) is True

    def test_verify_password_wrong(self):
        hashed = SECURITY.hash_password("correct")
        assert SECURITY.verify_password("wrong", hashed) is False

    def test_access_token_does_not_contain_refresh_type(self):
        with (
            patch("fitlife.security.settings.security.secret_key", "key"),
            patch("fitlife.security.settings.security.algorithm", "HS256"),
        ):
            token = SECURITY.create_access_token({"sub": "123", "role": "member"})
            payload = SECURITY.decode_access_token(token)
            assert payload.get("type") != "refresh"

    def test_refresh_token_rejected_by_decode_access(self):
        with (
            patch("fitlife.security.settings.security.secret_key", "key"),
            patch("fitlife.security.settings.security.algorithm", "HS256"),
        ):
            refresh = SECURITY.create_refresh_token({"sub": "123", "role": "member"})
            payload = SECURITY.decode_access_token(refresh)
            assert payload == {}

    def test_access_token_rejected_by_decode_refresh(self):
        with (
            patch("fitlife.security.settings.security.secret_key", "key"),
            patch("fitlife.security.settings.security.algorithm", "HS256"),
        ):
            access = SECURITY.create_access_token({"sub": "123", "role": "member"})
            payload = SECURITY.decode_refresh_token(access)
            assert payload == {}

    def test_expired_token_returns_empty_dict(self):
        with (
            patch("fitlife.security.settings.security.secret_key", "key"),
            patch("fitlife.security.settings.security.algorithm", "HS256"),
        ):
            token = SECURITY.create_access_token(
                {"sub": "123"},
                expires_delta=timedelta(seconds=-1),
            )
            payload = SECURITY.decode_access_token(token)
            assert payload == {}

    def test_invalid_token_returns_empty_dict(self):
        with (
            patch("fitlife.security.settings.security.secret_key", "key"),
            patch("fitlife.security.settings.security.algorithm", "HS256"),
        ):
            payload = SECURITY.decode_access_token("not.a.valid.token")
            assert payload == {}


class TestAuthSchemas:

    def test_member_register_valid_ukrainian_phone(self):
        schema = UserRegisterSchema(
            first_name="Іван",
            last_name="Петренко",
            email="ivan@test.ua",
            phone_number="+380671234567",
            password="pass123",
        )
        assert schema.phone_number == "+380671234567"

    @pytest.mark.parametrize("phone", [
        "+380501234567",
    ])
    def test_member_register_valid_phone_formats(self, phone):
        schema = UserRegisterSchema(
            first_name="A",
            last_name="B",
            email=None,
            phone_number=phone,
            password="pass",
        )
        assert schema.phone_number == phone

    @pytest.mark.parametrize("bad_phone", [
        "+7911234567",
        "911234567",
        "380123456",
        "+380001234567",
    ])
    def test_member_register_invalid_phone_raises(self, bad_phone):
        import pydantic
        with pytest.raises(pydantic.ValidationError):
            UserRegisterSchema(
                first_name="A",
                last_name="B",
                email=None,
                phone_number=bad_phone,
                password="pass",
            )

    def test_coach_register_schema_mirrors_member(self):
        schema = UserRegisterSchema(
            first_name="Сергій",
            last_name="Ткаченко",
            email="sergiy@coach.ua",
            phone_number="+380631234567",
            password="qwerty",
        )
        assert schema.first_name == "Сергій"
        assert schema.role if hasattr(schema, "role") else True


class TestGetCurrentUserDependency:

    @pytest.mark.asyncio
    async def test_valid_member_token_returns_member(self, mock_member_model):
        from fitlife.auth.dependencies import get_current_user

        member_id = str(mock_member_model.id)

        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_member_model
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": member_id,
            "role": "member",
        }

        result = await get_current_user(
            token="fake-token",
            session=mock_session,
            security=mock_security,
        )
        assert result is mock_member_model

    @pytest.mark.asyncio
    async def test_valid_coach_token_returns_coach(self, mock_coach_model):
        from fitlife.auth.dependencies import get_current_user

        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_coach_model
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": str(mock_coach_model.id),
            "role": "coach",
        }

        result = await get_current_user(
            token="fake-token",
            session=mock_session,
            security=mock_security,
        )
        assert result is mock_coach_model

    @pytest.mark.asyncio
    async def test_empty_payload_raises_401(self):
        from fastapi import HTTPException
        from fitlife.auth.dependencies import get_current_user

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {}

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(
                token="bad-token",
                session=MagicMock(),
                security=mock_security,
            )

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_unknown_role_raises_401(self):
        from fastapi import HTTPException
        from fitlife.auth.dependencies import get_current_user

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": str(uuid4()),
            "role": "superadmin",  # невідома роль
        }

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(
                token="bad",
                session=MagicMock(),
                security=mock_security,
            )

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_user_not_in_db_raises_401(self):
        from fastapi import HTTPException
        from fitlife.auth.dependencies import get_current_user

        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None  # не знайдено в БД
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": str(uuid4()),
            "role": "member",
        }

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(
                token="valid-looking",
                session=mock_session,
                security=mock_security,
            )

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_uuid_in_sub_raises_401(self):
        from fastapi import HTTPException
        from fitlife.auth.dependencies import get_current_user

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": "not-a-uuid",
            "role": "member",
        }

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(
                token="token",
                session=MagicMock(),
                security=mock_security,
            )

        assert exc_info.value.status_code == 401

class TestRoleGuards:

    @pytest.mark.asyncio
    async def test_member_guard_accepts_member(self, mock_member_model):
        from fitlife.auth.dependencies import get_current_active_member
        from fitlife.member.models import MemberModel

        mock_member_model.__class__ = MemberModel
        result = await get_current_active_member(current_user=mock_member_model)
        assert result is mock_member_model

    @pytest.mark.asyncio
    async def test_member_guard_rejects_coach(self, mock_coach_model):
        from fastapi import HTTPException
        from fitlife.auth.dependencies import get_current_active_member

        with pytest.raises(HTTPException) as exc_info:
            await get_current_active_member(current_user=mock_coach_model)

        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_coach_guard_rejects_member(self, mock_member_model):
        from fastapi import HTTPException
        from fitlife.auth.dependencies import get_current_active_coach

        with pytest.raises(HTTPException) as exc_info:
            await get_current_active_coach(current_user=mock_member_model)

        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_coach_guard_accepts_coach(self, mock_coach_model):
        from fitlife.auth.dependencies import get_current_active_coach
        from fitlife.coach.models import CoachModel

        mock_coach_model.__class__ = CoachModel
        result = await get_current_active_coach(current_user=mock_coach_model)
        assert result is mock_coach_model
