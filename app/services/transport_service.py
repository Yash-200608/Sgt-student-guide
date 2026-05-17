from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.transport import TransportOut
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id

COLLECTION_NAME = "transport"
LEGACY_COLLECTION_NAME = "bus_routes"


def _collection(collection_name: str = COLLECTION_NAME):
    return get_collection(collection_name)


def _normalize_transport(document: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(document)
    stops = normalized.get("stops")

    if not normalized.get("route"):
        normalized["route"] = normalized.get("route_number") or normalized.get("route_name")
    if not normalized.get("name"):
        normalized["name"] = normalized.get("route_name") or normalized.get("route_number")
    if not normalized.get("from") and isinstance(stops, list) and stops:
        normalized["from"] = stops[0]
    if not normalized.get("to") and isinstance(stops, list) and stops:
        normalized["to"] = stops[-1]
    if not normalized.get("morning"):
        normalized["morning"] = normalized.get("departure_time")
    if not normalized.get("evening"):
        normalized["evening"] = normalized.get("arrival_time")

    return normalized


def _format_transport(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transport route not found.",
        )

    normalized = _normalize_transport(serialized)
    return TransportOut.model_validate(normalized).model_dump(mode="json", by_alias=True)


async def _list_from_collection(collection_name: str) -> list[dict[str, Any]]:
    cursor = _collection(collection_name).find({}).sort([("route", 1), ("name", 1), ("route_number", 1)])
    documents = await cursor.to_list(length=None)
    return serialize_documents(documents)


async def get_all_transport() -> list[dict[str, Any]]:
    documents = await _list_from_collection(COLLECTION_NAME)
    if not documents:
        documents = await _list_from_collection(LEGACY_COLLECTION_NAME)

    return [_format_transport(document) for document in documents]


async def get_transport_by_id(transport_id: str) -> dict[str, Any]:
    object_id = validate_object_id(transport_id)
    document = await _collection().find_one({"_id": object_id})
    if document is None:
        document = await _collection(LEGACY_COLLECTION_NAME).find_one({"_id": object_id})

    return _format_transport(document)
