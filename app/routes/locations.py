from typing import Any

from fastapi import APIRouter

from app.services import location_service
from app.utils.response import success_response

router = APIRouter(tags=["Locations"])


@router.get("/locations")
@router.get("/api/locations", include_in_schema=False)
async def get_locations() -> dict[str, Any]:
    data = await location_service.get_all_locations()
    return success_response("Locations retrieved successfully.", data)


@router.get("/locations/{id}")
@router.get("/api/locations/{id}", include_in_schema=False)
async def get_location(id: str) -> dict[str, Any]:
    data = await location_service.get_location_by_id(id)
    return success_response("Location retrieved successfully.", data)
