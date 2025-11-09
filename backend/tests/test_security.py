from datetime import timedelta

import pytest

from fitlife.security import create_access_token, get_password_hash, verify_password


def test_password_hashing():
    """Test password hashing functionality."""
    password = "testpassword123"
    hashed = get_password_hash(password)

    # Hash should be different from plain password
    assert hashed != password

    # Hash should be bcrypt format
    assert hashed.startswith("$2b$")

    # Should be able to verify the password
    assert verify_password(password, hashed) is True


def test_password_verification_wrong_password():
    """Test password verification with wrong password."""
    password = "correctpassword"
    wrong_password = "wrongpassword"
    hashed = get_password_hash(password)

    assert verify_password(wrong_password, hashed) is False


def test_password_hash_uniqueness():
    """Test that same password generates different hashes (due to salt)."""
    password = "samepassword"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Hashes should be different due to salt
    assert hash1 != hash2

    # But both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_create_access_token_default_expiry():
    """Test creating access token with default expiry."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0

    # Decode and verify token
    from jose import jwt

    from fitlife.config import settings

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload


def test_create_access_token_custom_expiry():
    """Test creating access token with custom expiry."""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=60)
    token = create_access_token(data, expires_delta=expires_delta)

    assert isinstance(token, str)

    # Decode and verify token
    from jose import jwt

    from fitlife.config import settings

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload


def test_create_access_token_with_additional_claims():
    """Test creating access token with additional claims."""
    data = {"sub": "test@example.com", "role": "manager", "user_id": "123"}
    token = create_access_token(data)

    from jose import jwt

    from fitlife.config import settings

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert payload["role"] == "manager"
    assert payload["user_id"] == "123"


def test_token_verification_invalid_signature():
    """Test that token with invalid signature fails verification."""
    from jose import JWTError, jwt

    from fitlife.config import settings

    data = {"sub": "test@example.com"}
    token = create_access_token(data)

    # Try to decode with wrong secret
    with pytest.raises(JWTError):
        jwt.decode(token, "wrong_secret_key", algorithms=[settings.ALGORITHM])


def test_token_verification_invalid_algorithm():
    """Test that token with invalid algorithm fails verification."""
    from jose import JWTError, jwt

    from fitlife.config import settings

    data = {"sub": "test@example.com"}
    token = create_access_token(data)

    # Try to decode with wrong algorithm
    with pytest.raises(JWTError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
