from typing import Any

from fastapi import APIRouter, Depends, Query

from app.dependencies.auth import get_current_user
from app.services import notification_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("")
async def get_notifications(
    unread_only: bool = Query(default=False),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await notification_service.get_notifications(current_user, unread_only)
    return success_response("Notifications retrieved successfully.", data)


@router.put("/{id}/read")
async def mark_notification_read(
    id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await notification_service.mark_notification_read(id, current_user)
    return success_response("Notification marked as read.", data)
