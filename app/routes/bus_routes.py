from typing import Any

from fastapi import APIRouter

from app.services import bus_route_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/bus-routes", tags=["Bus Routes"])


@router.get("")
async def get_bus_routes() -> dict[str, Any]:
    data = await bus_route_service.get_all_bus_routes()
    return success_response("Bus routes retrieved successfully.", data)


@router.get("/{id}")
async def get_bus_route(id: str) -> dict[str, Any]:
    data = await bus_route_service.get_bus_route_by_id(id)
    return success_response("Bus route retrieved successfully.", data)
