from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class RecipientInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value: raise ValueError("name must not be blank")
        return value

class JobCreate(BaseModel):
    course_name: str = Field(min_length=1, max_length=200, alias="coursename")
    issue_date: date = Field(alias="issuedate")
    recipients: list[RecipientInput] = Field(min_length=1)
    model_config = ConfigDict(populate_by_name=True)
    @field_validator("course_name")
    @classmethod
    def course_not_blank(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value: raise ValueError("course name must not be blank")
        return value

class JobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    total_count: int
    successful_count: int
    failed_count: int
    pending_count: int
    processing_count: int
    progress_percentage: float
    results_url: str

class RecipientResponse(BaseModel):
    result_id: str
    name: str
    status: str
    certificate_id: str | None = None
    failure_code: str | None = None
    failure_message: str | None = None

class ResultsResponse(BaseModel):
    items: list[RecipientResponse]
    total: int
    offset: int
    limit: int
