from typing import Any

from fastapi import APIRouter, Query

from app.services import search_service
from app.utils.response import success_response

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("")
async def search(q: str = Query(..., min_length=2)) -> dict[str, Any]:
    data = await search_service.global_search(q)
    return success_response("Search completed successfully.", data)
