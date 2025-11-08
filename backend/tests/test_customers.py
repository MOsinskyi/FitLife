import pytest
from fastapi import status


def test_create_customer(client, manager_token):
    """Test creating a new customer."""
    response = client.post(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "newcustomer@test.com",
            "first_name": "New",
            "last_name": "Customer",
            "phone": "9876543210",
            "password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newcustomer@test.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "Customer"
    assert data["role"] == "customer"
    assert "id" in data


def test_get_customers_list(client, customer_token, sample_customer):
    """Test getting list of customers."""
    response = client.get(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_customer_by_id(client, customer_token, sample_customer):
    """Test getting a specific customer by ID."""
    customer_id = sample_customer["id"]
    response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == customer_id
    assert data["email"] == "customer@test.com"


def test_get_nonexistent_customer(client, customer_token):
    """Test getting a non-existent customer."""
    response = client.get(
        "/api/v1/customers/nonexistent-id",
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_customer_duplicate_email(client, manager_token, sample_customer):
    """Test creating a customer with duplicate email."""
    response = client.post(
        "/api/v1/customers",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={
            "email": "customer@test.com",  # Same email as sample_customer
            "first_name": "Duplicate",
            "last_name": "Customer",
            "phone": "9876543210",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_unauthorized_access_to_customers(client):
    """Test accessing customers endpoint without authentication."""
    response = client.get("/api/v1/customers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
