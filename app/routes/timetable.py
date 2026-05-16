from typing import Any

from fastapi import APIRouter, status

from app.schemas.timetable import TimetableCreate
from app.services import timetable_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/timetable", tags=["Timetable"])


@router.get("")
async def get_timetable() -> dict[str, Any]:
    data = await timetable_service.get_all_timetable_entries()
    return success_response("Timetable entries retrieved successfully.", data)


@router.get("/{day}")
async def get_timetable_by_day(day: str) -> dict[str, Any]:
    data = await timetable_service.get_timetable_entries_by_day(day)
    return success_response("Timetable entries retrieved successfully.", data)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_timetable_entry(payload: TimetableCreate) -> dict[str, Any]:
    data = await timetable_service.create_timetable_entry(payload)
    return success_response("Timetable entry created successfully.", data)


@router.delete("/{id}")
async def delete_timetable_entry(id: str) -> dict[str, Any]:
    await timetable_service.delete_timetable_entry(id)
    return success_response(
        "Timetable entry deleted successfully.",
        {"id": id},
    )
