from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, min_length=1, max_length=50)
    color: str | None = Field(default=None, max_length=30)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TaskTagLink(SQLModel, table=True):
    __tablename__ = "task_tag_links"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete="CASCADE")
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")
