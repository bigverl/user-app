import datetime

from app.users.models import User, UserRole

# Placeholder hash strings, not real bcrypt output -- security.py isn't wired up yet.
users: dict[int, User] = {
    1: User(
        user_id=1,
        username="admin_user",
        email="admin@example.com",
        hashed_password="$2b$12$placeholderhashvalue000000000000000000000000000000",
        role=UserRole.admin,
        created_at=datetime.datetime(2026, 8, 20, 9, 0, tzinfo=datetime.UTC),
    ),
    2: User(
        user_id=2,
        username="editor_user",
        email="editor@example.com",
        hashed_password="$2b$12$placeholderhashvalue111111111111111111111111111111",
        role=UserRole.editor,
        created_at=datetime.datetime(2026, 8, 21, 13, 45, tzinfo=datetime.UTC),
    ),
    3: User(
        user_id=3,
        username="viewer_user",
        email="viewer@example.com",
        hashed_password="$2b$12$placeholderhashvalue222222222222222222222222222222",
        role=UserRole.viewer,
        created_at=datetime.datetime(2026, 8, 22, 8, 30, tzinfo=datetime.UTC),
    ),
}
