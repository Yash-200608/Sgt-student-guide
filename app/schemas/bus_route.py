from pydantic import BaseModel, ConfigDict, Field


class BusRouteOut(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    route_name: str = Field(..., min_length=1, max_length=120)
    route_number: str = Field(..., min_length=1, max_length=50)
    stops: list[str] = Field(default_factory=list)
    departure_time: str | None = Field(default=None, max_length=50)
    arrival_time: str | None = Field(default=None, max_length=50)
    driver_name: str | None = Field(default=None, max_length=120)
    contact_number: str | None = Field(default=None, max_length=30)
