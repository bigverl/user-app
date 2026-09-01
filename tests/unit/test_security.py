from datetime import timedelta

import jwt
import pytest

from app.auth.security import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_password_hash,
    hash_password,
    verify_password,
)
from app.users.models import UserCreate


class TestHashPassword:
    def test_returns_a_different_string(self):
        assert hash_password("pw123") != "pw123"

    def test_two_hashes_of_same_password_differ(self):
        assert hash_password("pw123") != hash_password("pw123")


class TestGetPasswordHash:
    def test_round_trips_with_verify_password(self):
        hashed = get_password_hash("pw123")
        assert verify_password("pw123", hashed)

    def test_wrong_password_fails(self):
        hashed = get_password_hash("pw123")
        assert not verify_password("wrong", hashed)


class TestAuthenticateUser:
    def test_wrong_username_returns_none(self, service):
        assert authenticate_user("nobody", "whatever", service) is None

    def test_correct_credentials_return_user(self, service):
        service.create(
            UserCreate(username="dave", email="dave@example.com", password="pw123")
        )
        user = authenticate_user("dave", "pw123", service)
        assert user is not None
        assert user.username == "dave"

    def test_wrong_password_returns_none(self, service):
        service.create(
            UserCreate(username="dave", email="dave@example.com", password="pw123")
        )
        assert authenticate_user("dave", "wrong", service) is None


class TestCreateAccessToken:
    def test_encodes_the_given_claims(self):
        token = create_access_token(data={"sub": "1"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "1"

    def test_includes_an_expiry_claim(self):
        token = create_access_token(data={"sub": "1"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_expired_token_fails_to_decode(self):
        token = create_access_token(
            data={"sub": "1"}, expiration_delta=timedelta(seconds=-1)
        )
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
