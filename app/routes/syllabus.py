from typing import Any

from fastapi import APIRouter

from app.services import syllabus_service
from app.utils.response import success_response

router = APIRouter(tags=["Syllabus"])


@router.get("/syllabus")
@router.get("/api/syllabus", include_in_schema=False)
async def get_syllabus() -> dict[str, Any]:
    data = await syllabus_service.get_all_syllabus()
    return success_response("Syllabus retrieved successfully.", data)


@router.get("/syllabus/{id}")
@router.get("/api/syllabus/{id}", include_in_schema=False)
async def get_syllabus_item(id: str) -> dict[str, Any]:
    data = await syllabus_service.get_syllabus_by_id(id)
    return success_response("Syllabus item retrieved successfully.", data)
