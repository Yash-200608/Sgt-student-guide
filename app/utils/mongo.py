from collections.abc import Mapping, Sequence
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


def serialize_value(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, tuple):
        return [serialize_value(item) for item in value]
    if isinstance(value, Mapping):
        return {
            "id" if key == "_id" else key: serialize_value(item)
            for key, item in value.items()
        }

    return value


def serialize_document(document: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if document is None:
        return None

    return serialize_value(document)


def serialize_documents(documents: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [serialized for doc in documents if (serialized := serialize_document(doc))]


def validate_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resource id.",
        ) from None
