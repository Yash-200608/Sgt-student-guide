from typing import Any

from fastapi import APIRouter, status

from app.schemas.notice import NoticeCreate
from app.services import notice_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/notices", tags=["Notices"])


@router.get("")
async def get_notices() -> dict[str, Any]:
    data = await notice_service.get_all_notices()
    return success_response("Notices retrieved successfully.", data)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_notice(payload: NoticeCreate) -> dict[str, Any]:
    data = await notice_service.create_notice(payload)
    return success_response("Notice created successfully.", data)
