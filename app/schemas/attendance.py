from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, model_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AttendanceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    user_id: str = Field(..., min_length=1)
    course: str = Field(..., min_length=1, max_length=120)
    total_classes: int = Field(..., ge=0)
    attended_classes: int = Field(..., ge=0)
    department: str | None = Field(default=None, max_length=100)
    semester: int | None = Field(default=None, ge=1, le=12)

    @model_validator(mode="after")
    def validate_attendance_counts(self) -> "AttendanceCreate":
        if self.attended_classes > self.total_classes:
            raise ValueError("attended_classes cannot be greater than total_classes.")
        return self


class AttendanceOut(AttendanceCreate):
    id: str
    percentage: float
    updated_at: datetime
