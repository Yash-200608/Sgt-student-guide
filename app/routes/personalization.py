from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.preference import PreferenceUpdate
from app.services import (
    bookmark_service,
    dashboard_service,
    notice_service,
    preference_service,
    timetable_service,
)
from app.utils.response import success_response

router = APIRouter(tags=["Personalization"])


@router.get("/api/dashboard/me")
async def get_my_dashboard(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await dashboard_service.get_personal_dashboard(current_user)
    return success_response("Dashboard data retrieved successfully.", data)


@router.get("/api/timetable/me")
async def get_my_timetable(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await timetable_service.get_personalized_timetable(current_user)
    return success_response("Personalized timetable retrieved successfully.", data)


@router.get("/api/notices/me")
async def get_my_notices(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await notice_service.get_personalized_notices(current_user)
    return success_response("Personalized notices retrieved successfully.", data)


@router.post("/api/events/bookmark/{id}")
async def bookmark_event(
    id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await bookmark_service.bookmark_event(current_user["id"], id)
    return success_response("Event bookmarked successfully.", data)


@router.delete("/api/events/bookmark/{id}")
async def remove_bookmark(
    id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await bookmark_service.remove_bookmark(current_user["id"], id)
    return success_response("Event bookmark removed successfully.", data)


@router.get("/api/preferences")
async def get_preferences(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await preference_service.get_preferences(current_user["id"])
    return success_response("Preferences retrieved successfully.", data)


@router.put("/api/preferences")
async def update_preferences(
    payload: PreferenceUpdate,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await preference_service.update_preferences(current_user["id"], payload)
    return success_response("Preferences updated successfully.", data)
