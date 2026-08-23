# from typing import Annotated, Any

# from fastapi import APIRouter, Depends, HTTPException, Request
# from fastapi.security import APIKeyHeader
from fastapi import Request

# from app.models import user imports
from app.users.service import UserService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service
