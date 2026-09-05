from fastapi import Request

from app.events.dispatcher import Dispatcher


def get_dispatcher(request: Request) -> Dispatcher:
    return request.app.state.dispatcher
