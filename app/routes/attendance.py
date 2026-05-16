from typing import Any

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user, require_admin
from app.schemas.attendance import AttendanceCreate
from app.services import attendance_service
from app.utils.response import success_response

router = APIRouter(tags=["Attendance"])


@router.get("/api/attendance/me")
async def get_my_attendance(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    data = await attendance_service.get_attendance_for_user(current_user["id"])
    return success_response("Attendance retrieved successfully.", data)


@router.post(
    "/api/admin/attendance",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def upsert_attendance(payload: AttendanceCreate) -> dict[str, Any]:
    data = await attendance_service.upsert_attendance(payload)
    return success_response("Attendance record saved successfully.", data)
