from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True