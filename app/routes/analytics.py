from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_admin
from app.services import analytics_service
from app.utils.response import success_response

router = APIRouter(
    prefix="/api/admin/analytics",
    tags=["Analytics"],
    dependencies=[Depends(require_admin)],
)


@router.get("")
async def get_admin_analytics() -> dict[str, Any]:
    data = await analytics_service.get_admin_analytics()
    return success_response("Analytics retrieved successfully.", data)
