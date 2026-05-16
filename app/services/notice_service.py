from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.notice import NoticeCreate, NoticeOut, NoticeUpdate
from app.utils.mongo import serialize_document, serialize_documents
from app.utils.update import build_update_data

COLLECTION_NAME = "notices"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_notice(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load notice.",
        )

    return NoticeOut.model_validate(serialized).model_dump(mode="json")


def _format_notices(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        NoticeOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_all_notices() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort("created_at", -1)
    documents = await cursor.to_list(length=None)
    return _format_notices(documents)


async def get_personalized_notices(user: dict[str, Any]) -> list[dict[str, Any]]:
    filters: list[dict[str, Any]] = [
        {"is_global": True},
        {"is_global": {"$exists": False}},
    ]

    if user.get("department"):
        filters.append({"target_departments": user["department"]})
    if user.get("semester") is not None:
        filters.append({"target_semesters": user["semester"]})

    cursor = _collection().find({"$or": filters}).sort("created_at", -1)
    documents = await cursor.to_list(length=None)
    return _format_notices(documents)


async def create_notice(payload: NoticeCreate) -> dict[str, Any]:
    result = await _collection().insert_one(payload.model_dump(mode="python"))
    document = await _collection().find_one({"_id": result.inserted_id})
    return _format_notice(document)


async def update_notice(notice_id: str, payload: NoticeUpdate) -> dict[str, Any]:
    from app.utils.mongo import validate_object_id

    object_id = validate_object_id(notice_id)
    update_data = build_update_data(payload)
    result = await _collection().update_one({"_id": object_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found.",
        )

    document = await _collection().find_one({"_id": object_id})
    return _format_notice(document)
