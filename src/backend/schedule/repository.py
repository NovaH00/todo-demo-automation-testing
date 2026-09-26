from datetime import UTC, datetime

from sqlmodel import Session, col, select

from backend.tasks.models import Task


def get_tasks_in_range(
    session: Session, start_datetime: datetime, end_datetime: datetime
) -> list[Task]:
    statement = (
        select(Task)
        .where(
            col(Task.due_date).is_not(None),
            col(Task.due_date) >= start_datetime,
            col(Task.due_date) <= end_datetime,
        )
        .order_by(col(Task.due_date).asc())
    )
    return list(session.exec(statement).all())


def get_overdue_tasks(session: Session, current_time: datetime) -> list[Task]:
    statement = (
        select(Task)
        .where(
            col(Task.due_date).is_not(None),
            col(Task.due_date) < current_time,
            col(Task.is_completed).is_(False),
        )
        .order_by(col(Task.due_date).asc())
    )
    return list(session.exec(statement).all())


def batch_reschedule(
    session: Session, task_ids: list[int], new_due_date: datetime | None
) -> list[Task]:
    updated_tasks: list[Task] = []
    for task_id in task_ids:
        task = session.get(Task, task_id)
        if task:
            task.due_date = new_due_date
            task.updated_at = datetime.now(UTC)
            session.add(task)
            updated_tasks.append(task)
    session.commit()
    for task in updated_tasks:
        session.refresh(task)
    return updated_tasks
