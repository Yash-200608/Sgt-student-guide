from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.location import LocationOut
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id

COLLECTION_NAME = "locations"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_location(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found.",
        )

    return LocationOut.model_validate(serialized).model_dump(mode="json")


async def get_all_locations() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort([("block", 1), ("building", 1), ("name", 1)])
    documents = await cursor.to_list(length=None)
    return [
        LocationOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_location_by_id(location_id: str) -> dict[str, Any]:
    object_id = validate_object_id(location_id)
    document = await _collection().find_one({"_id": object_id})
    return _format_location(document)
