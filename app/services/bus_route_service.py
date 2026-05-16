from typing import Any

from fastapi import HTTPException, status

from app.config.database import get_collection
from app.schemas.bus_route import BusRouteOut
from app.utils.mongo import serialize_document, serialize_documents, validate_object_id

COLLECTION_NAME = "bus_routes"


def _collection():
    return get_collection(COLLECTION_NAME)


def _format_bus_route(document: dict[str, Any] | None) -> dict[str, Any]:
    serialized = serialize_document(document)
    if serialized is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus route not found.",
        )
    return BusRouteOut.model_validate(serialized).model_dump(mode="json")


async def get_all_bus_routes() -> list[dict[str, Any]]:
    cursor = _collection().find({}).sort("route_number", 1)
    documents = await cursor.to_list(length=None)
    return [
        BusRouteOut.model_validate(document).model_dump(mode="json")
        for document in serialize_documents(documents)
    ]


async def get_bus_route_by_id(route_id: str) -> dict[str, Any]:
    object_id = validate_object_id(route_id)
    document = await _collection().find_one({"_id": object_id})
    return _format_bus_route(document)
