import re
from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.timetable import TimetableCreate, TimetableOut, TimetableUpdate
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id
from app.utils.update import build_update_data

COLLECTION_NAME = "timetable"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_timetable_entry(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load timetable entry.",
        )

    return TimetableOut.model_validate(serialized).model_dump(mode="json")


def _format_timetable_entries(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        TimetableOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_all_timetable_entries() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort([("day", 1), ("time", 1)])
    documents = await cursor.to_list(length=None)
    return _format_timetable_entries(documents)


async def get_timetable_entries_by_day(day: str) -> list[dict[str, Any]]:
    normalized_day = day.strip()
    if not normalized_day:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Day cannot be empty.",
        )

    query = {"day": {"$regex": f"^{re.escape(normalized_day)}$", "$options": "i"}}
    cursor = _collection().find(query).sort("time", 1)
    documents = await cursor.to_list(length=None)
    return _format_timetable_entries(documents)


async def get_personalized_timetable(user: dict[str, Any]) -> list[dict[str, Any]]:
    filters: list[dict[str, Any]] = []

    if user.get("section"):
        filters.append({"section": {"$regex": f"^{re.escape(user['section'])}$", "$options": "i"}})
    if user.get("department"):
        filters.append(
            {
                "$or": [
                    {"department": user["department"]},
                    {"department": {"$exists": False}},
                    {"department": None},
                ]
            }
        )
    if user.get("semester") is not None:
        filters.append(
            {
                "$or": [
                    {"semester": user["semester"]},
                    {"semester": {"$exists": False}},
                    {"semester": None},
                ]
            }
        )

    query = {"$and": filters} if filters else {}
    cursor = _collection().find(query).sort([("day", 1), ("time", 1)])
    documents = await cursor.to_list(length=None)
    return _format_timetable_entries(documents)


async def create_timetable_entry(payload: TimetableCreate) -> dict[str, Any]:
    result = await _collection().insert_one(payload.model_dump(mode="python"))
    document = await _collection().find_one({"_id": result.inserted_id})
    return _format_timetable_entry(document)


async def update_timetable_entry(entry_id: str, payload: TimetableUpdate) -> dict[str, Any]:
    object_id = validate_object_id(entry_id)
    update_data = build_update_data(payload)
    result = await _collection().update_one({"_id": object_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable entry not found.",
        )

    document = await _collection().find_one({"_id": object_id})
    return _format_timetable_entry(document)


async def delete_timetable_entry(entry_id: str) -> None:
    object_id = validate_object_id(entry_id)
    result = await _collection().delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable entry not found.",
        )
