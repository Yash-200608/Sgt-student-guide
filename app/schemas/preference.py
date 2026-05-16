from pydantic import BaseModel, ConfigDict, Field


class PreferenceUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    theme: str | None = Field(default=None, min_length=1, max_length=30)
    notifications_enabled: bool | None = None
    default_dashboard_view: str | None = Field(default=None, min_length=1, max_length=50)
    favorite_clubs: list[str] | None = None


class PreferenceOut(BaseModel):
    id: str
    user_id: str
    theme: str = "system"
    notifications_enabled: bool = True
    default_dashboard_view: str = "overview"
    favorite_clubs: list[str] = Field(default_factory=list)
