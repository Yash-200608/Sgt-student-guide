from pydantic import BaseModel, ConfigDict, Field


class SyllabusOut(BaseModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    id: str
    name: str | None = Field(default=None, min_length=1, max_length=150)
    subject: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=3000)
    semester: int | str | None = Field(default=None)
    code: str | None = Field(default=None, min_length=1, max_length=50)
