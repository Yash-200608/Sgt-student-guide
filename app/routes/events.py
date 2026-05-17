from typing import Any

from fastapi import APIRouter, status

from app.schemas.event import EventCreate
from app.services import event_service
from app.utils.response import success_response

router = APIRouter(tags=["Events"])


@router.get("/events")
@router.get("/api/events", include_in_schema=False)
async def get_events() -> dict[str, Any]:
    data = await event_service.get_all_events()
    return success_response("Events retrieved successfully.", data)


@router.post("/api/events", status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate) -> dict[str, Any]:
    data = await event_service.create_event(payload)
    return success_response("Event created successfully.", data)


@router.delete("/api/events/{id}")
async def delete_event(id: str) -> dict[str, Any]:
    await event_service.delete_event(id)
    return success_response("Event deleted successfully.", {"id": id})
