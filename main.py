from enum import Enum

from fastapi import FastAPI


class UserRole(str, Enum):
    viewer = "viewer"
    editor = "editor"
    admin = "admin"


app = FastAPI()
