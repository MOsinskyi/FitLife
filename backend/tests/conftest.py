from datetime import timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from fitlife.security import Security

COACH_ID = uuid4()
MEMBER_ID = uuid4()
SESSION_ID = uuid4()

SECURITY = Security()
SECRET_KEY = "test-secret-key"
ALGORITHM = "HS256"


def make_token(user_id, role: str) -> str:
    with (
        patch("fitlife.security.settings.security.secret_key", SECRET_KEY),
        patch("fitlife.security.settings.security.algorithm", ALGORITHM),
    ):
        return SECURITY.create_access_token(
            data={"sub": str(user_id), "role": role},
            expires_delta=timedelta(minutes=30),
        )


@pytest.fixture
def coach_token() -> str:
    return make_token(COACH_ID, "coach")


@pytest.fixture
def member_token() -> str:
    return make_token(MEMBER_ID, "member")


@pytest.fixture
def mock_coach_model():
    coach = MagicMock()
    coach.id = COACH_ID
    coach.first_name = "Ivan"
    coach.last_name = "Kovalenko"
    coach.email = "ivan@gym.ua"
    coach.phone_number = "+380671234567"
    coach.role = "coach"
    coach.password = SECURITY.hash_password("secret")
    return coach


@pytest.fixture
def mock_member_model():
    member = MagicMock()
    member.id = MEMBER_ID
    member.first_name = "Olha"
    member.last_name = "Shevchenko"
    member.email = "olha@gym.ua"
    member.phone_number = "+380501234567"
    member.role = "member"
    member.password = SECURITY.hash_password("secret")
    return member


@pytest.fixture
def mock_training_session(mock_coach_model, mock_member_model):
    ts = MagicMock()
    ts.id = SESSION_ID
    ts.title = "Ранкова йога"
    ts.description = "Заняття з йоги для початківців"
    ts.max_participants = 10
    ts.duration_minutes = 60
    ts.price = 200
    ts.coach_id = COACH_ID
    ts.coach = mock_coach_model
    ts.members = []
    return ts
