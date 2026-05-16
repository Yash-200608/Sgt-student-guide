import re
from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.teacher import TeacherCreate, TeacherOut, TeacherUpdate
from app.utils.mongo import serialize_document, serialize_documents
from app.utils.mongo import validate_object_id
from app.utils.update import build_update_data

COLLECTION_NAME = "teachers"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_teacher(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load teacher.",
        )

    return TeacherOut.model_validate(serialized).model_dump(mode="json")


def _format_teachers(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        TeacherOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_all_teachers() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort("name", 1)
    documents = await cursor.to_list(length=None)
    return _format_teachers(documents)


async def get_teachers_by_department(department: str) -> list[dict[str, Any]]:
    normalized_department = department.strip()
    if not normalized_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department cannot be empty.",
        )

    query = {
        "department": {
            "$regex": f"^{re.escape(normalized_department)}$",
            "$options": "i",
        }
    }
    cursor = _collection().find(query).sort("name", 1)
    documents = await cursor.to_list(length=None)
    return _format_teachers(documents)


async def create_teacher(payload: TeacherCreate) -> dict[str, Any]:
    result = await _collection().insert_one(payload.model_dump(mode="python"))
    document = await _collection().find_one({"_id": result.inserted_id})
    return _format_teacher(document)


async def update_teacher(teacher_id: str, payload: TeacherUpdate) -> dict[str, Any]:
    object_id = validate_object_id(teacher_id)
    update_data = build_update_data(payload)
    result = await _collection().update_one({"_id": object_id}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found.",
        )

    document = await _collection().find_one({"_id": object_id})
    return _format_teacher(document)
