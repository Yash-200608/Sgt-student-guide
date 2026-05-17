from pydantic import BaseModel, ConfigDict, Field


class ClubBase(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=100, examples=["Coding Club"])
    description: str = Field(..., min_length=1, max_length=2000)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    coordinator: str | None = Field(default=None, min_length=1, max_length=120)
    meeting_time: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        examples=["Fridays, 4:00 PM"],
    )


class ClubCreate(ClubBase):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ClubOut(ClubBase):
    id: str


class ClubUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    coordinator: str | None = Field(default=None, min_length=1, max_length=120)
    meeting_time: str | None = Field(default=None, min_length=1, max_length=100)
