from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.club import ClubCreate, ClubOut, ClubUpdate
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id
from app.utils.update import build_update_data

COLLECTION_NAME = "clubs"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_club(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load club.",
        )

    return ClubOut.model_validate(serialized).model_dump(mode="json")


def _format_clubs(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        ClubOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_all_clubs() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort("name", 1)
    documents = await cursor.to_list(length=None)
    return _format_clubs(documents)


async def create_club(payload: ClubCreate) -> dict[str, Any]:
    result = await _collection().insert_one(payload.model_dump(mode="python"))
    document = await _collection().find_one({"_id": result.inserted_id})
    return _format_club(document)


async def update_club(club_id: str, payload: ClubUpdate) -> dict[str, Any]:
    object_id = validate_object_id(club_id)
    update_data = build_update_data(payload)
    result = await _collection().update_one({"_id": object_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found.",
        )

    document = await _collection().find_one({"_id": object_id})
    return _format_club(document)
