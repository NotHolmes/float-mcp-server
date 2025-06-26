from pydantic import BaseModel, Field
from typing import Optional


class LoggedTimeCreate(BaseModel):
    people_id: int = Field(..., gt=0)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    reference_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    hours: float = Field(..., ge=0, le=24)
    notes: Optional[str] = None
    project_id: int = Field(..., gt=0)
    phase_id: Optional[int] = Field(0, ge=0)
    task_id: Optional[int] = Field(None, gt=0)
    task_name: Optional[str] = None
    task_meta_id: Optional[int] = Field(None, gt=0)


class LoggedTimeResponse(LoggedTimeCreate):
    logged_time_id: str
    billable: Optional[int] = None
    locked: Optional[int] = 0
    created: Optional[str] = None
    created_by: Optional[int] = None
    modified: Optional[str] = None
    modified_by: Optional[int] = None
