from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    viewer = "viewer"
    editor = "editor"
    admin = "admin"

class User(BaseModel):
    user_id: int
    username: str
    email: str
    hashed_password: str
    role: UserRole
    created_at: datetime

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    email: str
    role: UserRole
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: UserRole | None = None