from typing import Any

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.schemas.user import UserCreate, UserLogin
from app.services import auth_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate) -> dict[str, Any]:
    data = await auth_service.signup(payload)
    return success_response("User registered successfully.", data)


@router.post("/login")
async def login(payload: UserLogin) -> dict[str, Any]:
    data = await auth_service.login(payload)
    return success_response("Login successful.", data)


@router.get("/profile")
async def get_profile(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    return success_response("Profile retrieved successfully.", current_user)
