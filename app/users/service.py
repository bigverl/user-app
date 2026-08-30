from app.users.models import User, UserRole, UserPublic, UserCreate, UserUpdate
from app.users.storage import users
from datetime import datetime, UTC
from app.auth.security import hash_password

class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class UserService:

    def __init__(self) -> None:
        """
        load users from storage.py
        """
        self.users: dict[int, User] = {
            user_id: user.model_copy() 
            for user_id, user 
            in users.items()
            }
        self.id_counter = len(self.users) # keep track of auto-incrementing user_id


    def create(self, new_user: UserCreate) -> UserPublic:
        """
        for simplicity, set default role to viewer. 
        update() will change it
        """

        hashed_password = hash_password(new_user.password)
        user = User(
            user_id= self.id_counter + 1,
            username = new_user.username,
            email = new_user.email,
            hashed_password=hashed_password,
            role = UserRole("viewer"),
            created_at = datetime.now(tz=UTC),
        )

        self.users[user.user_id] = user

        self.id_counter+= 1

        return UserPublic.model_validate(user)
    
    def get_list(self) -> list[UserPublic]:
        """
        return all users
        """
        return [
            UserPublic.model_validate(user)
            for user in self.users.values()
        ]

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
        if update.role is not None:
            user.role = update.role

        return UserPublic.model_validate(user)

    def delete(self, user_id: int) -> None:
        """
        remove a user by id
        """
        if self.users.pop(user_id, None) is None:
            raise UserNotFoundError(f"user {user_id} not found")