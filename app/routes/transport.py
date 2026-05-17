from typing import Any

from fastapi import APIRouter

from app.services import transport_service
from app.utils.response import success_response

router = APIRouter(tags=["Transport"])


@router.get("/transport")
@router.get("/api/transport", include_in_schema=False)
@router.get("/api/bus-routes", include_in_schema=False)
async def get_transport() -> dict[str, Any]:
    data = await transport_service.get_all_transport()
    return success_response("Transport routes retrieved successfully.", data)


@router.get("/transport/{id}")
@router.get("/api/transport/{id}", include_in_schema=False)
@router.get("/api/bus-routes/{id}", include_in_schema=False)
async def get_transport_route(id: str) -> dict[str, Any]:
    data = await transport_service.get_transport_by_id(id)
    return success_response("Transport route retrieved successfully.", data)
