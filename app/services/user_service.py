from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.user import UserOut
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id

COLLECTION_NAME = "users"


def _collection():
    return get_collection(COLLECTION_NAME)


def format_user(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    serialized.pop("password_hash", None)
    return UserOut.model_validate(serialized).model_dump(mode="json")


async def get_user_document_by_email(email: str) -> dict[str, Any] | None:
    return await _collection().find_one({"email": email.lower()})


async def get_user_document_by_id(user_id: str) -> dict[str, Any] | None:
    object_id = validate_object_id(user_id)
    return await _collection().find_one({"_id": object_id})


async def get_user_by_id(user_id: str) -> dict[str, Any]:
    document = await get_user_document_by_id(user_id)
    return format_user(document)


async def get_all_users() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort("created_at", -1)
    documents = await cursor.to_list(length=None)
    users = []
    for document in serialize_documents(documents):
        document.pop("password_hash", None)
        users.append(UserOut.model_validate(document).model_dump(mode="json"))
    return users
