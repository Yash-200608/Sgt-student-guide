from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.notification import NotificationCreate, NotificationOut
from app.utils.mongo import serialize_document, validate_object_id

COLLECTION_NAME = "notifications"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_notification(document: dict[str, Any], user_id: str) -> dict[str, Any]:
    serialized = serialize_document(document) or {}
    read_by = serialized.pop("read_by", [])
    serialized["is_read"] = user_id in read_by
    return NotificationOut.model_validate(serialized).model_dump(mode="json")


def _visibility_query(user: dict[str, Any]) -> dict[str, Any]:
    return {
        "$or": [
            {"user_id": user["id"]},
            {"target_roles": user["role"]},
            {"user_id": None, "target_roles": {"$size": 0}},
        ]
    }


async def create_notification(payload: NotificationCreate) -> dict[str, Any]:
    data = payload.model_dump(mode="python")
    data["target_roles"] = [role.value for role in payload.target_roles]
    data["read_by"] = []
    result = await _collection().insert_one(data)
    document = await _collection().find_one({"_id": result.inserted_id})
    return serialize_document(document) or {}


async def get_notifications(
    user: dict[str, Any],
    unread_only: bool = False,
) -> list[dict[str, Any]]:
    query = _visibility_query(user)
    if unread_only:
        query = {"$and": [query, {"read_by": {"$ne": user["id"]}}]}

    cursor = _collection().find(query).sort("created_at", -1)
    documents = await cursor.to_list(length=None)
    return [_format_notification(document, user["id"]) for document in documents]


async def mark_notification_read(notification_id: str, user: dict[str, Any]) -> dict[str, Any]:
    object_id = validate_object_id(notification_id)
    result = await _collection().update_one(
        {"_id": object_id, **_visibility_query(user)},
        {"$addToSet": {"read_by": user["id"]}},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    document = await _collection().find_one({"_id": object_id})
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )
    return _format_notification(document, user["id"])
