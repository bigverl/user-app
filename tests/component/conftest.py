import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.users.models import User
from app.users.router import get_user_service
from app.users.service import UserService


@pytest.fixture
def client(seed_users: dict[int, User]):
    service = UserService()
    service.users = seed_users
    app.dependency_overrides[get_user_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()
