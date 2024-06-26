from database import User
from auth.base_config import auth_backend
from fastapi_users import FastAPIUsers, fastapi_users
import uuid
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from typing import List, Optional
from pydantic.fields import Field
from enum import Enum
from datetime import datetime
from operations.router import router as router_operations
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI(
    title="Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"


app.include_router(router_operations)

