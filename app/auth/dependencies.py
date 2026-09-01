from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.auth.models import TokenData
from app.config import get_settings
from app.users.dependencies import get_user_service
from app.users.models import UserPublic
from app.users.service import UserNotFoundError, UserService

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(get_user_service),
) -> UserPublic:
    """
    resolve the current user from a bearer token, or raise 401
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # pull user id (sub) from jwt payload
        user_id = payload.get("sub")

        # case 1: invalid sub
        if user_id is None:
            raise credentials_exception

        # case 2: invalid shape or datatype
        token_data = TokenData(user_id=user_id)

    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    try:
        user = user_service.get_one(int(token_data.user_id))
    # case 3: user not found
    except UserNotFoundError:
        raise credentials_exception

    # case 4: all good
    return user
