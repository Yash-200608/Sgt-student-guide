from collections.abc import Mapping
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


def serialize_document(document: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if document is None:
        return None

    serialized = dict(document)
    serialized["id"] = str(serialized.pop("_id"))
    return serialized


def serialize_documents(documents: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [serialized for doc in documents if (serialized := serialize_document(doc))]


def validate_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resource id.",
        ) from None
