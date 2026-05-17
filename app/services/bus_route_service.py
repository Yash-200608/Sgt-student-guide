from typing import Any

from app.services.transport_service import get_all_transport, get_transport_by_id


async def get_all_bus_routes() -> list[dict[str, Any]]:
    return await get_all_transport()


async def get_bus_route_by_id(route_id: str) -> dict[str, Any]:
    return await get_transport_by_id(route_id)
