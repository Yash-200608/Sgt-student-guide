from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel


def build_update_data(payload: BaseModel) -> dict[str, Any]:
    update_data = payload.model_dump(mode="python", exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update.",
        )
    return update_data
