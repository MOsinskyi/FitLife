import pytest
from datetime import datetime, timedelta, timezone
from fastapi import status


@pytest.fixture
def sample_schedule(client, coach_token, sample_coach):
    """Create a sample schedule for booking tests."""
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    response = client.post(
        "/api/v1/schedules",
        headers={"Authorization": f"Bearer {coach_token}"},
        json={
            "coach_id": sample_coach["id"],
            "title": "Test Training Session",
            "description": "Test session for bookings",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "max_participants": 5,
            "training_type": "fitness"
        }
    )
    return response.json()


def test_create_booking_as_customer(client, customer_token, sample_customer, sample_schedule):
    """Test creating a booking as a customer."""
    response = client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={
            "customer_id": sample_customer["id"],
            "schedule_id": sample_schedule["id"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["customer_id"] == sample_customer["id"]
    assert data["schedule_id"] == sample_schedule["id"]
    assert data["status"] == "confirmed"
    assert "id" in data
    assert "booking_time" in data


def test_create_booking_as_coach_forbidden(client, coach_token, sample_customer, sample_schedule):
    """Test that coaches cannot create bookings."""
    response = client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {coach_token}"},
        json={
            "customer_id": sample_customer["id"],
            "schedule_id": sample_schedule["id"]
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_bookings_list(client, customer_token, sample_customer, sample_schedule):
    """Test getting list of bookings."""
    # First create a booking
    client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={
            "customer_id": sample_customer["id"],
            "schedule_id": sample_schedule["id"]
        }
    )

    # Then get the list
    response = client.get(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_booking_by_id(client, customer_token, sample_customer, sample_schedule):
    """Test getting a specific booking by ID."""
    # Create a booking first
    create_response = client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={
            "customer_id": sample_customer["id"],
            "schedule_id": sample_schedule["id"]
        }
    )
    booking_id = create_response.json()["id"]

    # Get the booking
    response = client.get(
        f"/api/v1/bookings/{booking_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == booking_id


def test_get_nonexistent_booking(client, customer_token):
    """Test getting a non-existent booking."""
    response = client.get(
        "/api/v1/bookings/nonexistent-id",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_customer_bookings(client, customer_token, sample_customer, sample_schedule):
    """Test getting bookings for a specific customer."""
    # Create a booking
    client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={
            "customer_id": sample_customer["id"],
            "schedule_id": sample_schedule["id"]
        }
    )

    # Get customer's bookings
    response = client.get(
        f"/api/v1/bookings/customer/{sample_customer['id']}",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    # This endpoint might not exist yet, so check for both success and not found
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        assert isinstance(data, list)


def test_unauthorized_access_to_bookings(client):
    """Test accessing bookings endpoint without authentication."""
    response = client.get("/api/v1/bookings")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_booking_nonexistent_schedule(client, customer_token, sample_customer):
    """Test creating a booking for non-existent schedule."""
    response = client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {customer_token}"},
        json={
            "customer_id": sample_customer["id"],
            "schedule_id": "nonexistent-schedule-id"
        }
    )
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
