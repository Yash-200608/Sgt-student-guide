from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventBase(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=150, examples=["Tech Fest"])
    date: datetime | str = Field(..., examples=["2026-06-01T10:00:00Z"])
    description: str = Field(..., min_length=1, max_length=2000)
    location: str | None = Field(default=None, min_length=1, max_length=150)
    venue: str | None = Field(default=None, min_length=1, max_length=150)
    time: str | None = Field(default=None, min_length=1, max_length=80)
    category: str | None = Field(default=None, min_length=1, max_length=80)


class EventCreate(EventBase):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @model_validator(mode="after")
    def require_location_or_venue(self) -> "EventCreate":
        if not self.location and not self.venue:
            raise ValueError("Either location or venue is required.")
        return self


class EventOut(EventBase):
    id: str


class EventUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    date: datetime | str | None = None
    location: str | None = Field(default=None, min_length=1, max_length=150)
    venue: str | None = Field(default=None, min_length=1, max_length=150)
    time: str | None = Field(default=None, min_length=1, max_length=80)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
