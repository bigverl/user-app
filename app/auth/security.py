from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import bcrypt
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from app.config import get_settings
from app.users.models import User

if TYPE_CHECKING:
    from app.users.service import UserService

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

password_hash = PasswordHash((BcryptHasher(),))
DUMMY_HASH = password_hash.hash("dummypassword")


# on create
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(
    username: str,
    password: str,
    service: UserService,
) -> User | None:
    """
    look up a user by username and verify their password, or return None
    """

    user = service.get_by_name(username)

    # case 1: user not found
    if user is None:
        verify_password(password, DUMMY_HASH)
        return None

    # case 2: user found, password correct
    if verify_password(password, user.hashed_password):
        return user

    # case 3: user found, password incorrect
    return None


def create_access_token(
    data: dict,
    expiration_delta: timedelta | None = None,
) -> str:
    """
    encode claims into a signed, expiring JWT
    """

    if expiration_delta is not None:
        expire = datetime.now(UTC) + expiration_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)

    jwt_data = data.copy()
    jwt_data.update({"exp": expire})
    encoded_jwt = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
