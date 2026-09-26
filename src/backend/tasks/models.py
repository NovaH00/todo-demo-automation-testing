from datetime import UTC, datetime

from sqlmodel import Field, SQLModel

from backend.tasks.constants import TaskPriority


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=200)
    description: str | None = Field(default=None)
    is_completed: bool = Field(default=False, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = Field(default=None)
    list_id: int | None = Field(default=None, foreign_key="lists.id", index=True)
    recurrence: str = Field(default="none")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
