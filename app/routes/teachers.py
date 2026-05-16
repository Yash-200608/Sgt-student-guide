from typing import Any

from fastapi import APIRouter, status

from app.schemas.teacher import TeacherCreate
from app.services import teacher_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])


@router.get("")
async def get_teachers() -> dict[str, Any]:
    data = await teacher_service.get_all_teachers()
    return success_response("Teachers retrieved successfully.", data)


@router.get("/{department}")
async def get_teachers_by_department(department: str) -> dict[str, Any]:
    data = await teacher_service.get_teachers_by_department(department)
    return success_response("Teachers retrieved successfully.", data)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_teacher(payload: TeacherCreate) -> dict[str, Any]:
    data = await teacher_service.create_teacher(payload)
    return success_response("Teacher created successfully.", data)
