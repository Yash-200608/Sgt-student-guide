from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.event import EventCreate, EventOut, EventUpdate
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id
from app.utils.update import build_update_data

COLLECTION_NAME = "events"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_event(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load event.",
        )

    return EventOut.model_validate(serialized).model_dump(mode="json")


def _format_events(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        EventOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_all_events() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort("date", 1)
    documents = await cursor.to_list(length=None)
    return _format_events(documents)


async def get_event_by_id(event_id: str) -> dict[str, Any]:
    object_id = validate_object_id(event_id)
    document = await _collection().find_one({"_id": object_id})
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return _format_event(document)


async def create_event(payload: EventCreate) -> dict[str, Any]:
    result = await _collection().insert_one(payload.model_dump(mode="python"))
    document = await _collection().find_one({"_id": result.inserted_id})
    return _format_event(document)


async def update_event(event_id: str, payload: EventUpdate) -> dict[str, Any]:
    object_id = validate_object_id(event_id)
    update_data = build_update_data(payload)
    result = await _collection().update_one({"_id": object_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    document = await _collection().find_one({"_id": object_id})
    return _format_event(document)


async def delete_event(event_id: str) -> None:
    object_id = validate_object_id(event_id)
    result = await _collection().delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
