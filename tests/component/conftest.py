import pytest
from fastapi.testclient import TestClient

from app.events.dependencies import get_dispatcher
from app.events.dispatcher import Dispatcher
from app.main import app
from app.users.models import User
from app.users.router import get_user_service
from app.users.service import UserService


@pytest.fixture
def client(seed_users: dict[int, User]):
    dispatcher = Dispatcher()
    service = UserService(dispatcher)
    service.users = seed_users
    app.dependency_overrides[get_user_service] = lambda: service
    app.dependency_overrides[get_dispatcher] = lambda: dispatcher
    yield TestClient(app)
    app.dependency_overrides.clear()
