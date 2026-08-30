import pytest

from app.users import storage
from app.users.models import User
from app.users.service import UserService


@pytest.fixture
def service(seed_users: dict[int, User]) -> UserService:
    storage.users.clear()
    storage.users.update(seed_users)
    return UserService()
