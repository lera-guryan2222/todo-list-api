from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    priority: str = Field("medium", pattern="^(low|medium|high)$")
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    priority: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
