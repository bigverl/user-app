from datetime import timedelta

import jwt
import pytest
from fastapi import HTTPException

from app.auth.dependencies import get_current_user
from app.auth.security import ALGORITHM, SECRET_KEY, create_access_token


class TestGetCurrentUser:
    def test_valid_token_returns_user(self, service):
        token = create_access_token(data={"sub": "1"})
        user = get_current_user(token, service)
        assert user.user_id == 1

    def test_garbage_token_raises_401(self, service):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("not-a-real-token", service)
        assert exc_info.value.status_code == 401

    def test_expired_token_raises_401(self, service):
        token = create_access_token(
            data={"sub": "1"}, expiration_delta=timedelta(seconds=-1)
        )
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token, service)
        assert exc_info.value.status_code == 401

    def test_missing_sub_raises_401(self, service):
        token = create_access_token(data={})
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token, service)
        assert exc_info.value.status_code == 401

    def test_non_string_sub_raises_401(self, service):
        token = jwt.encode({"sub": 123}, SECRET_KEY, algorithm=ALGORITHM)
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token, service)
        assert exc_info.value.status_code == 401

    def test_unknown_user_id_raises_401(self, service):
        token = create_access_token(data={"sub": "999"})
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token, service)
        assert exc_info.value.status_code == 401
