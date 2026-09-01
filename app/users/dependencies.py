from fastapi import Request

from app.users.service import UserService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service
