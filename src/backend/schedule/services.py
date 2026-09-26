from datetime import UTC, datetime, time, timedelta

from sqlmodel import Session

from backend.schedule import repository
from backend.schedule.schemas import RescheduleRequest, ScheduleOverview
from backend.tasks.models import Task
from backend.tasks.schemas import TaskRead


def get_today_bounds() -> tuple[datetime, datetime]:
    now = datetime.now(UTC)
    start = datetime.combine(now.date(), time.min, tzinfo=UTC)
    end = datetime.combine(now.date(), time.max, tzinfo=UTC)
    return start, end


def fetch_today_tasks(session: Session) -> list[Task]:
    start, end = get_today_bounds()
    return repository.get_tasks_in_range(session, start, end)


def fetch_overdue_tasks(session: Session) -> list[Task]:
    now = datetime.now(UTC)
    return repository.get_overdue_tasks(session, now)


def fetch_upcoming_tasks(session: Session, days: int = 7) -> list[Task]:
    now = datetime.now(UTC)
    end = now + timedelta(days=days)
    return repository.get_tasks_in_range(session, now, end)


def fetch_overview(session: Session) -> ScheduleOverview:
    today_tasks = fetch_today_tasks(session)
    overdue_tasks = fetch_overdue_tasks(session)
    upcoming_tasks = fetch_upcoming_tasks(session, days=7)

    return ScheduleOverview(
        overdue_count=len(overdue_tasks),
        today_count=len(today_tasks),
        upcoming_count=len(upcoming_tasks),
        tasks_today=[TaskRead.model_validate(t) for t in today_tasks],
        tasks_overdue=[TaskRead.model_validate(t) for t in overdue_tasks],
    )


def reschedule(session: Session, request: RescheduleRequest) -> list[Task]:
    return repository.batch_reschedule(
        session=session,
        task_ids=request.task_ids,
        new_due_date=request.new_due_date,
    )
