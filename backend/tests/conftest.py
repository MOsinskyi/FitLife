from datetime import UTC

import pytest
from fastapi.testclient import TestClient

from fitlife.database import (
    accounts_db,
    booking_db,
    coaches_db,
    customers_db,
    get_db,
    memberships_db,
    schedules_db,
)
from fitlife.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def clean_db():
    """Clean the database before each test."""
    accounts_db.clear()
    coaches_db.clear()
    customers_db.clear()
    memberships_db.clear()
    booking_db.clear()
    schedules_db.clear()
    yield
    # Cleanup after test
    accounts_db.clear()
    coaches_db.clear()
    customers_db.clear()
    memberships_db.clear()
    booking_db.clear()
    schedules_db.clear()


@pytest.fixture
def sample_manager(clean_db):
    """Create a sample manager user."""
    import uuid
    from datetime import datetime

    from fitlife.security import get_password_hash

    manager_id = str(uuid.uuid4())
    manager = {
        "id": manager_id,
        "email": "manager@test.com",
        "first_name": "Test",
        "last_name": "Manager",
        "phone": "1234567890",
        "hashed_password": get_password_hash("testpassword"),
        "role": "manager",
        "is_active": True,
        "created_at": datetime.now(UTC),
    }
    accounts_db["manager@test.com"] = manager
    return manager


@pytest.fixture
def sample_coach(clean_db):
    """Create a sample coach user."""
    from fitlife.user.repositories import UserRepository
    from fitlife.user.services import UserService

    db = get_db()
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    coach_data = {
        "email": "coach@test.com",
        "first_name": "Test",
        "last_name": "Coach",
        "phone": "1234567890",
        "password": "testpassword",
    }

    return user_service.register_coach(coach_data)


@pytest.fixture
def sample_customer(clean_db):
    """Create a sample customer user."""
    from fitlife.user.repositories import UserRepository
    from fitlife.user.services import UserService

    db = get_db()
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    customer_data = {
        "email": "customer@test.com",
        "first_name": "Test",
        "last_name": "Customer",
        "phone": "1234567890",
        "password": "testpassword",
    }

    return user_service.register_customer(customer_data)


@pytest.fixture
def manager_token(client, sample_manager):
    """Get authentication token for manager."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "manager@test.com", "password": "testpassword"}
    )
    return response.json()["access_token"]


@pytest.fixture
def coach_token(client, sample_coach):
    """Get authentication token for coach."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "coach@test.com", "password": "testpassword"}
    )
    return response.json()["access_token"]


@pytest.fixture
def customer_token(client, sample_customer):
    """Get authentication token for customer."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "customer@test.com", "password": "testpassword"}
    )
    return response.json()["access_token"]
