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
PATCH_MEMBER_REPO = "fitlife.members.repositories.MemberRepository"
PATCH_COACH_REPO = "fitlife.coaches.repositories.CoachRepository"

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
            password="password123",
        )
        assert schema.phone_number == "+380671234567"

    @pytest.mark.parametrize("phone", [
        "+380501234567",
    ])
    def test_member_register_valid_phone_formats(self, phone):
        schema = UserRegisterSchema(
            first_name="A",
            last_name="B",
            email="test@example.com",
            phone_number=phone,
            password="password123",
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
            password="password123",
        )
        assert schema.first_name == "Сергій"


class TestGetCurrentUserDependency:

    @pytest.mark.asyncio
    async def test_valid_member_token_returns_member(self, mock_member_model):
        from fitlife.auth.dependencies import get_current_user

        member_id = str(mock_member_model.id)

        mock_member_repo = MagicMock()
        mock_member_repo.get_user_by_id = AsyncMock(return_value=mock_member_model)

        mock_coach_repo = MagicMock()

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": member_id,
            "role": "member",
        }

        result = await get_current_user(
            member_repository=mock_member_repo,
            coach_repository=mock_coach_repo,
            security=mock_security,
            token="fake-token",
        )
        assert result is mock_member_model

    @pytest.mark.asyncio
    async def test_valid_coach_token_returns_coach(self, mock_coach_model):
        from fitlife.auth.dependencies import get_current_user

        mock_member_repo = MagicMock()
        mock_coach_repo = MagicMock()
        mock_coach_repo.get_user_by_id = AsyncMock(return_value=mock_coach_model)

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": str(mock_coach_model.id),
            "role": "coach",
        }

        result = await get_current_user(
            member_repository=mock_member_repo,
            coach_repository=mock_coach_repo,
            security=mock_security,
            token="fake-token",
        )
        assert result is mock_coach_model

    @pytest.mark.asyncio
    async def test_empty_payload_raises_exception(self):
        from fitlife.exceptions import InvalidCredentialsException
        from fitlife.auth.dependencies import get_current_user

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {}

        with pytest.raises(InvalidCredentialsException):
            await get_current_user(
                member_repository=MagicMock(),
                coach_repository=MagicMock(),
                security=mock_security,
                token="bad-token",
            )

    @pytest.mark.asyncio
    async def test_unknown_role_raises_exception(self):
        from fitlife.exceptions import InvalidCredentialsException
        from fitlife.auth.dependencies import get_current_user

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": str(uuid4()),
            "role": "superadmin",
        }

        with pytest.raises(InvalidCredentialsException):
            await get_current_user(
                member_repository=MagicMock(),
                coach_repository=MagicMock(),
                security=mock_security,
                token="bad",
            )

    @pytest.mark.asyncio
    async def test_user_not_in_db_raises_exception(self):
        from fitlife.exceptions import InvalidCredentialsException
        from fitlife.auth.dependencies import get_current_user

        mock_member_repo = MagicMock()
        mock_member_repo.get_user_by_id = AsyncMock(return_value=None)

        mock_security = MagicMock()
        mock_security.decode_access_token.return_value = {
            "sub": str(uuid4()),
            "role": "member",
        }

        with pytest.raises(InvalidCredentialsException):
            await get_current_user(
                member_repository=mock_member_repo,
                coach_repository=MagicMock(),
                security=mock_security,
                token="valid-looking",
            )

class TestUserRoles:

    def test_user_roles_enum_has_member_and_coach(self):
        from fitlife.schemas import UserRoles

        assert UserRoles.MEMBER.value == 'member'
        assert UserRoles.COACH.value == 'coach'
