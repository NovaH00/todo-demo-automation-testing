from datetime import UTC, datetime

from sqlmodel import Session, col, select

from backend.tags.models import TaskTagLink
from backend.tasks.constants import TaskPriority, TaskStatusFilter
from backend.tasks.models import Task
from backend.tasks.schemas import TaskCreate, TaskRead, TaskUpdate


def to_task_read(session: Session, task: Task) -> TaskRead:
    tag_ids: list[int] = []
    if task.id is not None:
        tag_ids = list(
            session.exec(
                select(TaskTagLink.tag_id).where(col(TaskTagLink.task_id) == task.id)
            ).all()
        )
    return TaskRead(
        id=task.id or 0,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        priority=task.priority,
        due_date=task.due_date,
        list_id=task.list_id,
        recurrence=task.recurrence,
        tag_ids=tag_ids,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def list_tasks(
    session: Session,
    status_filter: TaskStatusFilter = TaskStatusFilter.ALL,
    priority: TaskPriority | None = None,
    search: str | None = None,
    list_id: int | None = None,
    tag_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[Task]:
    statement = select(Task)

    if status_filter == TaskStatusFilter.PENDING:
        statement = statement.where(col(Task.is_completed).is_(False))
    elif status_filter == TaskStatusFilter.COMPLETED:
        statement = statement.where(col(Task.is_completed).is_(True))

    if priority is not None:
        statement = statement.where(col(Task.priority) == priority)

    if list_id is not None:
        statement = statement.where(col(Task.list_id) == list_id)

    if tag_id is not None:
        statement = statement.join(
            TaskTagLink, col(Task.id) == col(TaskTagLink.task_id)
        ).where(col(TaskTagLink.tag_id) == tag_id)

    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            col(Task.title).ilike(search_pattern)
            | (
                col(Task.description).is_not(None)
                & col(Task.description).ilike(search_pattern)
            )
        )

    if Task.id is not None:
        statement = statement.order_by(col(Task.id).desc())

    statement = statement.offset(offset).limit(limit)
    return list(session.exec(statement).all())


def create_task(session: Session, task_in: TaskCreate) -> Task:
    task_data = task_in.model_dump(exclude={"tag_ids"})
    task = Task.model_validate(task_data)
    session.add(task)
    session.commit()
    session.refresh(task)

    if task_in.tag_ids and task.id is not None:
        for tid in task_in.tag_ids:
            session.add(TaskTagLink(task_id=task.id, tag_id=tid))
        session.commit()

    return task


def update_task(session: Session, task: Task, task_in: TaskUpdate) -> Task:
    task_data = task_in.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for key, value in task_data.items():
        setattr(task, key, value)
    task.updated_at = datetime.now(UTC)
    session.add(task)

    if task_in.tag_ids is not None and task.id is not None:
        links = session.exec(
            select(TaskTagLink).where(col(TaskTagLink.task_id) == task.id)
        ).all()
        for link in links:
            session.delete(link)
        for tid in task_in.tag_ids:
            session.add(TaskTagLink(task_id=task.id, tag_id=tid))

    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()
