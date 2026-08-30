import datetime

import pytest

from app.users.models import User, UserRole


@pytest.fixture
def seed_users() -> dict[int, User]:
    return {
        1: User(
            user_id=1,
            username="admin_user",
            email="admin@example.com",
            hashed_password="hashed-admin-pw",
            role=UserRole.admin,
            created_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        ),
        2: User(
            user_id=2,
            username="editor_user",
            email="editor@example.com",
            hashed_password="hashed-editor-pw",
            role=UserRole.editor,
            created_at=datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC),
        ),
        3: User(
            user_id=3,
            username="viewer_user",
            email="viewer@example.com",
            hashed_password="hashed-viewer-pw",
            role=UserRole.viewer,
            created_at=datetime.datetime(2026, 1, 3, tzinfo=datetime.UTC),
        ),
    }
