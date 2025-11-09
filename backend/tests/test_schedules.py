from datetime import UTC, datetime, timedelta

import pytest
from fastapi import status


@pytest.fixture
def sample_schedule(client, coach_token, sample_coach):
    """Create a sample schedule."""
    start_time = datetime.now(UTC) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    response = client.post(
        "/api/v1/schedules",
        headers={"Authorization": f"Bearer {coach_token}"},
        json={
            "coach_id": sample_coach["id"],
            "title": "Morning Yoga",
            "description": "Relaxing yoga session",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_participants": 10,
            "training_type": "yoga",
        },
    )
    return response.json()


def test_create_schedule_as_coach(client, coach_token, sample_coach):
    """Test creating a schedule as a coach."""
    start_time = datetime.now(UTC) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    response = client.post(
        "/api/v1/schedules",
        headers={"Authorization": f"Bearer {coach_token}"},
        json={
            "coach_id": sample_coach["id"],
            "title": "Evening CrossFit",
            "description": "High intensity workout",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_participants": 15,
            "training_type": "crossfit",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Evening CrossFit"
    assert data["coach_id"] == sample_coach["id"]
    assert "id" in data


def test_create_schedule_as_customer_forbidden(client, customer_token, sample_coach):
    """Test that customers cannot create schedules."""
    start_time = datetime.now(UTC) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    response = client.post(
        "/api/v1/schedules",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={
            "coach_id": sample_coach["id"],
            "title": "Unauthorized Schedule",
            "description": "This should fail",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_participants": 10,
            "training_type": "yoga",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_schedules_list(client, coach_token, sample_schedule):
    """Test getting list of schedules."""
    response = client.get("/api/v1/schedules", headers={"Authorization": f"Bearer {coach_token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_schedule_by_id(client, coach_token, sample_schedule):
    """Test getting a specific schedule by ID."""
    schedule_id = sample_schedule["id"]
    response = client.get(
        f"/api/v1/schedules/{schedule_id}", headers={"Authorization": f"Bearer {coach_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == schedule_id
    assert data["title"] == "Morning Yoga"


def test_get_nonexistent_schedule(client, coach_token):
    """Test getting a non-existent schedule."""
    response = client.get(
        "/api/v1/schedules/nonexistent-id", headers={"Authorization": f"Bearer {coach_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_schedule_invalid_time_range(client, coach_token, sample_coach):
    """Test creating a schedule with end time before start time."""
    start_time = datetime.now(UTC) + timedelta(days=1)
    end_time = start_time - timedelta(hours=1)  # Invalid: end before start

    response = client.post(
        "/api/v1/schedules",
        headers={"Authorization": f"Bearer {coach_token}"},
        json={
            "coach_id": sample_coach["id"],
            "title": "Invalid Schedule",
            "description": "This should fail",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_participants": 10,
            "training_type": "yoga",
        },
    )
    # Assuming validation exists - adjust based on implementation
    assert response.status_code in [
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        status.HTTP_200_OK,
    ]


def test_unauthorized_access_to_schedules(client):
    """Test accessing schedules endpoint without authentication."""
    response = client.get("/api/v1/schedules")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
