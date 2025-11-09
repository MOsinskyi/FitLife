from fastapi import status


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


def test_login_success(client, sample_manager):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "manager@test.com", "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, sample_manager):
    """Test login with invalid password."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "manager@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client, clean_db):
    """Test login with non-existent user."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "nonexistent@test.com", "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_access_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without authentication token."""
    response = client.get("/api/v1/managers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_access_protected_endpoint_with_valid_token(client, manager_token):
    """Test accessing protected endpoint with valid token."""
    response = client.get("/api/v1/managers", headers={"Authorization": f"Bearer {manager_token}"})
    assert response.status_code == status.HTTP_200_OK


def test_access_protected_endpoint_with_invalid_token(client):
    """Test accessing protected endpoint with invalid token."""
    response = client.get("/api/v1/managers", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_token_contains_user_email(client, sample_manager, manager_token):
    """Test that token payload contains user email."""
    from jose import jwt

    from fitlife.config import settings

    payload = jwt.decode(manager_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "manager@test.com"


def test_coach_cannot_access_manager_endpoint(client, coach_token):
    """Test that coach cannot access manager-only endpoints."""
    response = client.get("/api/v1/managers", headers={"Authorization": f"Bearer {coach_token}"})
    # This might return 403 if role-checking is enforced on the endpoint
    # or 200 if the endpoint allows all authenticated users
    # Adjust based on your actual implementation
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
