from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.syllabus import SyllabusOut
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id

COLLECTION_NAME = "syllabus"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_syllabus(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Syllabus item not found.",
        )

    return SyllabusOut.model_validate(serialized).model_dump(mode="json")


async def get_all_syllabus() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort([("semester", 1), ("name", 1), ("subject", 1)])
    documents = await cursor.to_list(length=None)
    return [
        SyllabusOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_syllabus_by_id(syllabus_id: str) -> dict[str, Any]:
    object_id = validate_object_id(syllabus_id)
    document = await _collection().find_one({"_id": object_id})
    return _format_syllabus(document)
