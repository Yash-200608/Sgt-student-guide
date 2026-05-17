from pydantic import BaseModel, ConfigDict, Field


class TransportOut(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    id: str
    route: str | None = Field(default=None, min_length=1, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    from_location: str | None = Field(
        default=None,
        alias="from",
        min_length=1,
        max_length=150,
    )
    to: str | None = Field(default=None, min_length=1, max_length=150)
    morning: str | None = Field(default=None, min_length=1, max_length=80)
    evening: str | None = Field(default=None, min_length=1, max_length=80)
