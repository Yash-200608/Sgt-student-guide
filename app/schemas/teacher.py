from pydantic import BaseModel, ConfigDict, Field


class TeacherBase(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=100, examples=["Dr. Neha Verma"])
    department: str = Field(..., min_length=1, max_length=100, examples=["Computer Science"])
    cabin: str = Field(..., min_length=1, max_length=50, examples=["Faculty Block 2, Room 305"])
    email: str = Field(
        ...,
        min_length=3,
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        examples=["neha.verma@sgtuniversity.org"],
    )
    expertise: str | list[str] | None = Field(default=None)


class TeacherCreate(TeacherBase):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class TeacherOut(TeacherBase):
    id: str


class TeacherUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    cabin: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = Field(
        default=None,
        min_length=3,
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    expertise: str | list[str] | None = Field(default=None)
