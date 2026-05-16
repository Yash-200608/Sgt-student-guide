from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserRole


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class NotificationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=150)
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: str | None = None
    target_roles: list[UserRole] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class NotificationOut(BaseModel):
    id: str
    title: str
    message: str
    user_id: str | None = None
    target_roles: list[str] = Field(default_factory=list)
    is_read: bool = False
    created_at: datetime
