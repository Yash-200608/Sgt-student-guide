from typing import Any

from fastapi import APIRouter, status

from app.schemas.club import ClubCreate
from app.services import club_service
from app.utils.response import success_response

router = APIRouter(tags=["Clubs"])


@router.get("/clubs")
@router.get("/api/clubs", include_in_schema=False)
async def get_clubs() -> dict[str, Any]:
    data = await club_service.get_all_clubs()
    return success_response("Clubs retrieved successfully.", data)


@router.post("/api/clubs", status_code=status.HTTP_201_CREATED)
async def create_club(payload: ClubCreate) -> dict[str, Any]:
    data = await club_service.create_club(payload)
    return success_response("Club created successfully.", data)
