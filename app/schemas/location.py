from pydantic import BaseModel, ConfigDict, Field


class LocationOut(BaseModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    id: str
    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    block: str | None = Field(default=None, min_length=1, max_length=100)
    building: str | None = Field(default=None, min_length=1, max_length=100)
    floor: str | int | None = Field(default=None)
