from fastapi import status


def test_create_coach(client, manager_token):
    """Test creating a new coach."""
    response = client.post(
        "/api/v1/coaches",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "newcoach@test.com",
            "first_name": "New",
            "last_name": "Coach",
            "phone": "9876543210",
            "password": "newpassword123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newcoach@test.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "Coach"
    assert data["role"] == "coach"
    assert "id" in data


def test_get_coaches_list(client, coach_token, sample_coach):
    """Test getting list of coaches."""
    response = client.get("/api/v1/coaches", headers={"Authorization": f"Bearer {coach_token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_coach_by_id(client, coach_token, sample_coach):
    """Test getting a specific coach by ID."""
    coach_id = sample_coach["id"]
    response = client.get(
        f"/api/v1/coaches/{coach_id}", headers={"Authorization": f"Bearer {coach_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == coach_id
    assert data["email"] == "coach@test.com"


def test_get_nonexistent_coach(client, coach_token):
    """Test getting a non-existent coach."""
    response = client.get(
        "/api/v1/coaches/nonexistent-id", headers={"Authorization": f"Bearer {coach_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_coach_duplicate_email(client, manager_token, sample_coach):
    """Test creating a coach with duplicate email."""
    response = client.post(
        "/api/v1/coaches",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "coach@test.com",  # Same email as sample_coach
            "first_name": "Duplicate",
            "last_name": "Coach",
            "phone": "9876543210",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unauthorized_access_to_coaches(client):
    """Test accessing coaches endpoint without authentication."""
    response = client.get("/api/v1/coaches")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
