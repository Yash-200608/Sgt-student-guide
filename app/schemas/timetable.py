from pydantic import BaseModel, ConfigDict, Field, model_validator


class TimetableBase(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    day: str = Field(..., min_length=1, max_length=20, examples=["Monday"])
    time: str = Field(..., min_length=1, max_length=50, examples=["09:00 AM - 10:00 AM"])
    course: str | None = Field(default=None, min_length=1, max_length=120)
    subject: str | None = Field(default=None, min_length=1, max_length=120)
    teacher: str = Field(..., min_length=1, max_length=100, examples=["Dr. Sharma"])
    room: str = Field(..., min_length=1, max_length=50, examples=["B-204"])
    section: str | None = Field(default=None, min_length=1, max_length=50, examples=["CSE-A"])
    department: str | None = Field(default=None, max_length=100, examples=["Computer Science"])
    semester: int | None = Field(default=None, ge=1, le=12, examples=[5])


class TimetableCreate(TimetableBase):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @model_validator(mode="after")
    def require_course_or_subject(self) -> "TimetableCreate":
        if not self.course and not self.subject:
            raise ValueError("Either course or subject is required.")
        return self


class TimetableOut(TimetableBase):
    id: str


class TimetableUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    day: str | None = Field(default=None, min_length=1, max_length=20)
    time: str | None = Field(default=None, min_length=1, max_length=50)
    course: str | None = Field(default=None, min_length=1, max_length=120)
    subject: str | None = Field(default=None, min_length=1, max_length=120)
    teacher: str | None = Field(default=None, min_length=1, max_length=100)
    room: str | None = Field(default=None, min_length=1, max_length=50)
    section: str | None = Field(default=None, min_length=1, max_length=50)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    semester: int | None = Field(default=None, ge=1, le=12)
