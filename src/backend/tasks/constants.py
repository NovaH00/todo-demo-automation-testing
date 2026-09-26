from enum import StrEnum


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatusFilter(StrEnum):
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"
