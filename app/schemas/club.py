from pydantic import BaseModel, ConfigDict, Field


class ClubCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=100, examples=["Coding Club"])
    description: str = Field(..., min_length=1, max_length=2000)
    meeting_time: str = Field(..., min_length=1, max_length=100, examples=["Fridays, 4:00 PM"])


class ClubOut(ClubCreate):
    id: str


class ClubUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
    meeting_time: str | None = Field(default=None, min_length=1, max_length=100)
