from dataclasses import dataclass


# dataclass for internal domain model, not pydantic for dto
class Event:
    pass


@dataclass(frozen=True)
class UserCreatedEvent(Event):
    user_id: int


@dataclass(frozen=True)
class LoginEvent(Event):
    user_id: int


@dataclass(frozen=True)
class LoginFailedEvent(Event):
    username: str
