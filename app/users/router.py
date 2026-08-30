from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth.dependencies import get_current_user
from app.users.models import (
    UserCreate,
    UserPublic,
    UserRole,
    UserUpdate,
)
from app.users.service import UserService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


responses: dict[int | str, dict[str, Any]] = {
    200: {"description": "ok"},
    201: {"description": "created"},
    204: {"description": "no content"},  # delete
    400: {"description": "bad request"},
    401: {"description": "unauthorized"},
    403: {"description": "forbidden"},
    404: {"description": "not found"},
    422: {"description": "validation error"},
}


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses=responses,
)


@router.post("/", status_code=201)
async def create(
    new_user: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserPublic:
    """
    Create a new user.

    Implements: POST /users
    """
    return service.create(new_user)


@router.get("/")
async def get_list(
    service: UserService = Depends(get_user_service),
) -> list[UserPublic]:
    """
    List all users.

    Implements: GET /users
    """
    return service.get_list()


@router.get("/{user_id}")
async def get_one(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserPublic:
    """
    Return one user, full detail.

    Implements: GET /users/{user_id}
    """
    return service.get_one(user_id)


@router.patch("/{user_id}")
async def update(
    user_id: int,
    update: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: int = Depends(get_current_user),
) -> UserPublic:
    """
    Update a user's fields.

    Implements: PATCH /users/{user_id}
    """
    if update.role is not None and service.get_one(current_user).role is not UserRole(
        "admin"
    ):
        raise HTTPException(
            403,
            "insufficient permissions to edit user roles",
        )

    return service.update(user_id, update)


@router.delete("/{user_id}", status_code=204)
async def delete(
    user_id: int, service: UserService = Depends(get_user_service)
) -> None:
    """
    Delete a user.

    Implements: DELETE /users/{user_id}
    """
    service.delete(user_id)


# change password?
