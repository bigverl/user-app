from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler

from app.users.service import UserNotFoundError, UserService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.user_service = UserService()
    yield


USER_STATUS_CODES: dict[type[Exception], int] = {
    UserNotFoundError: 404,
    # InvalidUserInput: 400,
}


async def handle_user_error(request: Request, exc: Exception):
    status_code = USER_STATUS_CODES.get(type(exc), 500)
    return await http_exception_handler(
        request, HTTPException(status_code=status_code, detail=str(exc))
    )


app = FastAPI(lifespan=lifespan)
# app.include_router(user_router)
# app.include_router(auth_router)
# app.add_exception_handler(placeholder, handle_user_error)
