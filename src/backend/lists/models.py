from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class TodoList(SQLModel, table=True):
    __tablename__ = "lists"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    description: str | None = Field(default=None)
    color: str | None = Field(default=None, max_length=30)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
