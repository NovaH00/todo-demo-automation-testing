from fastapi import HTTPException, status
from sqlmodel import Session

from backend.tasks import repository
from backend.tasks.constants import TaskPriority, TaskStatusFilter
from backend.tasks.schemas import TaskCreate, TaskRead, TaskUpdate


def fetch_tasks(
    session: Session,
    status_filter: TaskStatusFilter = TaskStatusFilter.ALL,
    priority: TaskPriority | None = None,
    search: str | None = None,
    list_id: int | None = None,
    tag_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[TaskRead]:
    tasks = repository.list_tasks(
        session=session,
        status_filter=status_filter,
        priority=priority,
        search=search,
        list_id=list_id,
        tag_id=tag_id,
        offset=offset,
        limit=limit,
    )
    return [repository.to_task_read(session, task) for task in tasks]


def fetch_task_by_id(session: Session, task_id: int) -> TaskRead:
    task = repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return repository.to_task_read(session, task)


def create_new_task(session: Session, task_in: TaskCreate) -> TaskRead:
    task = repository.create_task(session, task_in)
    return repository.to_task_read(session, task)


def update_existing_task(
    session: Session, task_id: int, task_in: TaskUpdate
) -> TaskRead:
    task = repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    updated = repository.update_task(session, task, task_in)
    return repository.to_task_read(session, updated)


def remove_task(session: Session, task_id: int) -> None:
    task = repository.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    repository.delete_task(session, task)
