from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ListCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    color: str | None = Field(default=None, max_length=30)


class ListUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    color: str | None = Field(default=None, max_length=30)


class ListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    color: str | None = None
    task_count: int = 0
    created_at: datetime
    updated_at: datetime
