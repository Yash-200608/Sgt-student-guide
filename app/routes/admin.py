from typing import Any

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import require_admin
from app.schemas.club import ClubCreate, ClubUpdate
from app.schemas.event import EventCreate, EventUpdate
from app.schemas.notice import NoticeCreate, NoticeUpdate
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.schemas.timetable import TimetableCreate, TimetableUpdate
from app.services import (
    club_service,
    event_service,
    notice_service,
    teacher_service,
    timetable_service,
    user_service,
)
from app.utils.response import success_response

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate) -> dict[str, Any]:
    data = await event_service.create_event(payload)
    return success_response("Event created successfully.", data)


@router.put("/events/{id}")
async def update_event(id: str, payload: EventUpdate) -> dict[str, Any]:
    data = await event_service.update_event(id, payload)
    return success_response("Event updated successfully.", data)


@router.delete("/events/{id}")
async def delete_event(id: str) -> dict[str, Any]:
    await event_service.delete_event(id)
    return success_response("Event deleted successfully.", {"id": id})


@router.post("/notices", status_code=status.HTTP_201_CREATED)
async def create_notice(payload: NoticeCreate) -> dict[str, Any]:
    data = await notice_service.create_notice(payload)
    return success_response("Notice created successfully.", data)


@router.put("/notices/{id}")
async def update_notice(id: str, payload: NoticeUpdate) -> dict[str, Any]:
    data = await notice_service.update_notice(id, payload)
    return success_response("Notice updated successfully.", data)


@router.post("/timetable", status_code=status.HTTP_201_CREATED)
async def create_timetable_entry(payload: TimetableCreate) -> dict[str, Any]:
    data = await timetable_service.create_timetable_entry(payload)
    return success_response("Timetable entry created successfully.", data)


@router.put("/timetable/{id}")
async def update_timetable_entry(id: str, payload: TimetableUpdate) -> dict[str, Any]:
    data = await timetable_service.update_timetable_entry(id, payload)
    return success_response("Timetable entry updated successfully.", data)


@router.post("/teachers", status_code=status.HTTP_201_CREATED)
async def create_teacher(payload: TeacherCreate) -> dict[str, Any]:
    data = await teacher_service.create_teacher(payload)
    return success_response("Teacher created successfully.", data)


@router.put("/teachers/{id}")
async def update_teacher(id: str, payload: TeacherUpdate) -> dict[str, Any]:
    data = await teacher_service.update_teacher(id, payload)
    return success_response("Teacher updated successfully.", data)


@router.post("/clubs", status_code=status.HTTP_201_CREATED)
async def create_club(payload: ClubCreate) -> dict[str, Any]:
    data = await club_service.create_club(payload)
    return success_response("Club created successfully.", data)


@router.put("/clubs/{id}")
async def update_club(id: str, payload: ClubUpdate) -> dict[str, Any]:
    data = await club_service.update_club(id, payload)
    return success_response("Club updated successfully.", data)


@router.get("/users")
async def get_users() -> dict[str, Any]:
    data = await user_service.get_all_users()
    return success_response("Users retrieved successfully.", data)
