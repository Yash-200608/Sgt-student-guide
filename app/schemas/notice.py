from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class NoticeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=150, examples=["Semester Registration"])
    content: str = Field(..., min_length=1, max_length=3000)
    is_global: bool = True
    target_departments: list[str] = Field(default_factory=list)
    target_semesters: list[int] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class NoticeOut(NoticeCreate):
    id: str


class NoticeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    content: str | None = Field(default=None, min_length=1, max_length=3000)
    is_global: bool | None = None
    target_departments: list[str] | None = None
    target_semesters: list[int] | None = None
