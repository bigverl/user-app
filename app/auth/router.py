from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import Token
from app.auth.security import authenticate_user, create_access_token
from app.config import get_settings
from app.users.dependencies import get_user_service
from app.users.service import UserService

settings = get_settings()
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


responses: dict[int | str, dict[str, Any]] = {
    200: {"description": "ok"},
    401: {"description": "unauthorized"},
    422: {"description": "validation error"},
}

router = APIRouter(
    prefix="/token",
    tags=["token"],
    responses=responses,
)


@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> Token:
    """
    Verify credentials and issue an access token.

    Implements: POST /token
    """

    user = authenticate_user(
        form_data.username,
        form_data.password,
        user_service,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expiration_delta=access_token_expire_time,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


# Router end
