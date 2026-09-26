from datetime import datetime

from pydantic import BaseModel, Field

from backend.tasks.schemas import TaskRead


class ScheduleOverview(BaseModel):
    overdue_count: int
    today_count: int
    upcoming_count: int
    tasks_today: list[TaskRead]
    tasks_overdue: list[TaskRead]


class RescheduleRequest(BaseModel):
    task_ids: list[int] = Field(min_length=1)
    new_due_date: datetime | None = None
