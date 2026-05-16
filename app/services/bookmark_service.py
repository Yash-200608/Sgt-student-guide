from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.services.event_service import get_event_by_id
from app.utils.mongo import serialize_documents, validate_object_id

BOOKMARKS_COLLECTION = "bookmarks"
EVENTS_COLLECTION = "events"


def _bookmarks_collection():
    return get_collection(BOOKMARKS_COLLECTION)


def _events_collection():
    return get_collection(EVENTS_COLLECTION)


async def bookmark_event(user_id: str, event_id: str) -> dict[str, Any]:
    await get_event_by_id(event_id)
    await _bookmarks_collection().update_one(
        {"user_id": user_id, "event_id": event_id},
        {
            "$setOnInsert": {
                "user_id": user_id,
                "event_id": event_id,
                "created_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )
    return {"event_id": event_id, "bookmarked": True}


async def remove_bookmark(user_id: str, event_id: str) -> dict[str, Any]:
    result = await _bookmarks_collection().delete_one(
        {"user_id": user_id, "event_id": event_id}
    )
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmarked event not found.",
        )
    return {"event_id": event_id, "bookmarked": False}


async def get_bookmarked_events(user_id: str) -> list[dict[str, Any]]:
    bookmarks_cursor = _bookmarks_collection().find({"user_id": user_id}).sort(
        "created_at",
        -1,
    )
    bookmarks = await bookmarks_cursor.to_list(length=None)
    event_ids = []
    for bookmark in bookmarks:
        event_id = bookmark.get("event_id")
        if event_id:
            event_ids.append(validate_object_id(event_id))

    if not event_ids:
        return []

    events_cursor = _events_collection().find({"_id": {"$in": event_ids}})
    documents = await events_cursor.to_list(length=None)
    return serialize_documents(documents)
