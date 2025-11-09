from fastapi import status


def test_create_manager(client, manager_token):
    """Test creating a new manager."""
    response = client.post(
        "/api/v1/managers",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "newmanager@test.com",
            "first_name": "New",
            "last_name": "Manager",
            "phone": "9876543210",
            "password": "newpassword123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newmanager@test.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "Manager"
    assert data["role"] == "manager"
    assert "id" in data
    assert "password" not in data  # Password should not be returned


def test_get_managers_list(client, manager_token, sample_manager):
    """Test getting list of managers."""
    response = client.get("/api/v1/managers", headers={"Authorization": f"Bearer {manager_token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_manager_by_id(client, manager_token, sample_manager):
    """Test getting a specific manager by ID."""
    manager_id = sample_manager["id"]
    response = client.get(
        f"/api/v1/managers/{manager_id}", headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == manager_id
    assert data["email"] == "manager@test.com"


def test_get_nonexistent_manager(client, manager_token):
    """Test getting a non-existent manager."""
    response = client.get(
        "/api/v1/managers/nonexistent-id", headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_manager_duplicate_email(client, manager_token, sample_manager):
    """Test creating a manager with duplicate email."""
    response = client.post(
        "/api/v1/managers",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "manager@test.com",  # Same email as sample_manager
            "first_name": "Duplicate",
            "last_name": "Manager",
            "phone": "9876543210",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_manager_invalid_email(client, manager_token):
    """Test creating a manager with invalid email format."""
    response = client.post(
        "/api/v1/managers",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "Manager",
            "phone": "1234567890",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_unauthorized_access_to_managers(client):
    """Test accessing managers endpoint without authentication."""
    response = client.get("/api/v1/managers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
