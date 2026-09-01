from datetime import UTC, datetime

from app.auth.security import hash_password
from app.users.models import (
    User,
    UserCreate,
    UserPublic,
    UserRole,
    UserRoleUpdate,
    UserUpdate,
)
from app.users.storage import users


class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class UserService:
    def __init__(self) -> None:
        """
        load users from storage.py
        """
        # fmt: off
        self.users: dict[int, User] = {
            user_id: user.model_copy()
            for user_id, user in users.items()
        }
        # fmt: on
        self.id_counter = len(self.users)  # keep track of auto-incrementing user_id

    def create(self, new_user: UserCreate) -> UserPublic:
        """
        for simplicity, set default role to viewer.
        update() will change it
        """

        hashed_password = hash_password(new_user.password)
        user = User(
            user_id=self.id_counter + 1,
            username=new_user.username,
            email=new_user.email,
            hashed_password=hashed_password,
            role=UserRole("viewer"),
            created_at=datetime.now(tz=UTC),
        )

        self.users[user.user_id] = user

        self.id_counter += 1

        return UserPublic.model_validate(user)

    def get_list(self) -> list[UserPublic]:
        """
        return all users
        """
        # fmt: off
        return [
            UserPublic.model_validate(user)
            for user in self.users.values()
        ]
        # fmt: on

    def get_one(self, user_id: int) -> UserPublic:
        """
        return a single user by id, or raise UserNotFoundError
        """
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"user {user_id} not found")
        return UserPublic.model_validate(user)

    def update(self, user_id: int, update: UserUpdate) -> UserPublic:
        """
        update an existing user's fields
        """
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"user {user_id} not found")

        if update.username is not None:
            user.username = update.username
        if update.email is not None:
            user.email = update.email

        return UserPublic.model_validate(user)

    def update_role(self, user_id: int, role_update: UserRoleUpdate) -> UserPublic:
        """
        update an existing user's role
        """
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"user {user_id} not found")

        user.role = role_update.role

        return UserPublic.model_validate(user)

    def delete(self, user_id: int) -> None:
        """
        remove a user by id
        """
        if self.users.pop(user_id, None) is None:
            raise UserNotFoundError(f"user {user_id} not found")

    def get_by_name(self, username: str) -> User | None:
        """
        get user by name, or None if not found
        """
        for user in self.users.values():
            if user.username == username:
                return user

        return None
