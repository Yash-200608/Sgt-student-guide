from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=150, examples=["Tech Fest"])
    date: datetime = Field(..., examples=["2026-06-01T10:00:00Z"])
    location: str = Field(..., min_length=1, max_length=150, examples=["Main Auditorium"])
    description: str = Field(..., min_length=1, max_length=2000)


class EventOut(EventCreate):
    id: str


class EventUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    date: datetime | None = None
    location: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
