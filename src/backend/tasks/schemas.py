from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.tasks.constants import TaskPriority


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    is_completed: bool = False
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None
    list_id: int | None = None
    recurrence: str = "none"
    tag_ids: list[int] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    is_completed: bool | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    list_id: int | None = None
    recurrence: str | None = None
    tag_ids: list[int] | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    is_completed: bool
    priority: TaskPriority
    due_date: datetime | None = None
    list_id: int | None = None
    recurrence: str = "none"
    tag_ids: list[int] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
