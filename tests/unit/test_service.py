import pytest

from app.auth.security import verify_password
from app.users.models import UserCreate, UserPublic, UserRole, UserUpdate
from app.users.service import UserNotFoundError, UserService


class TestCreate:
    def test_assigns_incrementing_id_and_default_role(self, service):
        u = service.create(UserCreate(username="dave", email="dave@example.com", password="pw123"))
        assert u.user_id == 4  # seed data has ids 1-3
        assert u.role == UserRole.viewer

    def test_persists_into_users(self, service):
        u = service.create(UserCreate(username="dave", email="dave@example.com", password="pw123"))
        assert service.get_one(u.user_id).username == "dave"

    def test_hashes_the_password(self, service):
        u = service.create(UserCreate(username="dave", email="dave@example.com", password="pw123"))
        stored = service.users[u.user_id].hashed_password
        assert stored != "pw123"
        assert verify_password("pw123", stored)

    def test_returns_user_public_without_hashed_password(self, service):
        u = service.create(UserCreate(username="dave", email="dave@example.com", password="pw123"))
        assert isinstance(u, UserPublic)
        assert "hashed_password" not in u.model_dump()

    def test_second_create_increments_again(self, service):
        first = service.create(UserCreate(username="dave", email="dave@example.com", password="pw123"))
        second = service.create(UserCreate(username="erin", email="erin@example.com", password="pw456"))
        assert second.user_id == first.user_id + 1

    def test_instances_do_not_share_storage(self, service):
        service.create(UserCreate(username="dave", email="dave@example.com", password="pw123"))
        other = UserService()
        assert len(other.users) == 3
        with pytest.raises(UserNotFoundError):
            other.get_one(4)


class TestGetList:
    def test_returns_all(self, service):
        assert len(service.get_list()) == 3

    def test_returns_user_public_instances(self, service):
        assert all(isinstance(u, UserPublic) for u in service.get_list())

    def test_empty_when_no_users(self, service):
        service.users.clear()
        assert service.get_list() == []


class TestGetOne:
    def test_found(self, service):
        assert service.get_one(1).username == "admin_user"

    def test_missing_raises(self, service):
        with pytest.raises(UserNotFoundError):
            service.get_one(999)


class TestUpdate:
    def test_update_username(self, service):
        u = service.update(1, UserUpdate(username="new_name"))
        assert u.username == "new_name"

    def test_update_email(self, service):
        u = service.update(1, UserUpdate(email="new@example.com"))
        assert u.email == "new@example.com"

    def test_update_role(self, service):
        u = service.update(1, UserUpdate(role=UserRole.editor))
        assert u.role == UserRole.editor

    def test_partial_update_leaves_other_fields(self, service):
        before = service.get_one(1)
        u = service.update(1, UserUpdate(username="new_name"))
        assert u.email == before.email
        assert u.role == before.role

    def test_no_fields_set_is_a_no_op(self, service):
        before = service.get_one(1)
        u = service.update(1, UserUpdate())
        assert u == before

    def test_persists(self, service):
        service.update(1, UserUpdate(username="new_name"))
        assert service.get_one(1).username == "new_name"

    def test_missing_id_raises(self, service):
        with pytest.raises(UserNotFoundError):
            service.update(999, UserUpdate(username="new_name"))


class TestDelete:
    def test_removes_record(self, service):
        service.delete(1)
        assert 1 not in service.users

    def test_missing_id_raises(self, service):
        with pytest.raises(UserNotFoundError):
            service.delete(999)
