from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.attendance import AttendanceCreate, AttendanceOut
from app.services.user_service import get_user_by_id
from app.utils.mongo import serialize_document, serialize_documents

COLLECTION_NAME = "attendance"


def _collection():
    return get_collection(COLLECTION_NAME)


def _calculate_percentage(attended_classes: int, total_classes: int) -> float:
    if total_classes == 0:
        return 0.0
    return round((attended_classes / total_classes) * 100, 2)


def _format_attendance(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found.",
        )
    return AttendanceOut.model_validate(serialized).model_dump(mode="json")


async def get_attendance_for_user(user_id: str) -> list[dict[str, Any]]:
    cursor = _collection().find({"user_id": user_id}).sort("course", 1)
    documents = await cursor.to_list(length=None)
    return [
        AttendanceOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def upsert_attendance(payload: AttendanceCreate) -> dict[str, Any]:
    user = await get_user_by_id(payload.user_id)
    data = payload.model_dump(mode="python")
    data["department"] = payload.department or user.get("department")
    data["semester"] = payload.semester or user.get("semester")
    data["percentage"] = _calculate_percentage(
        payload.attended_classes,
        payload.total_classes,
    )
    data["updated_at"] = datetime.now(timezone.utc)

    await _collection().update_one(
        {"user_id": payload.user_id, "course": payload.course},
        {"$set": data},
        upsert=True,
    )
    document = await _collection().find_one(
        {"user_id": payload.user_id, "course": payload.course}
    )
    return _format_attendance(document)
