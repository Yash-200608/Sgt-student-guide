from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.config.settings import get_settings
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserRole
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password
from app.services.user_service import format_user, get_user_document_by_email

COLLECTION_NAME = "users"


def _collection():
    return get_collection(COLLECTION_NAME)


async def signup(payload: UserCreate) -> dict[str, Any]:
    if payload.role == UserRole.ADMIN and not get_settings().allow_admin_signup:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin signup is disabled.",
        )

    existing_user = await get_user_document_by_email(payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user_data = payload.model_dump(mode="python", exclude={"password"})
    user_data["password_hash"] = hash_password(payload.password)
    user_data["created_at"] = datetime.now(timezone.utc)

    result = await _collection().insert_one(user_data)
    document = await _collection().find_one({"_id": result.inserted_id})
    return format_user(document)


async def login(payload: UserLogin) -> dict[str, Any]:
    document = await get_user_document_by_email(payload.email)
    if document is None or not verify_password(payload.password, document["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = format_user(document)
    token = create_access_token(
        subject=user["id"],
        claims={"role": user["role"], "email": user["email"]},
    )

    response = TokenResponse(
        access_token=token,
        expires_in_minutes=get_settings().access_token_expire_minutes,
        user=user,
    )
    return response.model_dump(mode="json")
