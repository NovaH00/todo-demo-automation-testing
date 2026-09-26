from typing import Annotated

from fastapi import APIRouter, Query

from backend.schedule import services
from backend.schedule.schemas import RescheduleRequest, ScheduleOverview
from backend.tasks.dependencies import SessionDep
from backend.tasks.schemas import TaskRead

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/overview")
def get_schedule_overview(session: SessionDep) -> ScheduleOverview:
    return services.fetch_overview(session=session)


@router.get("/today")
def get_tasks_for_today(session: SessionDep) -> list[TaskRead]:
    tasks = services.fetch_today_tasks(session=session)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/overdue")
def get_overdue_tasks(session: SessionDep) -> list[TaskRead]:
    tasks = services.fetch_overdue_tasks(session=session)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/upcoming")
def get_upcoming_tasks(
    session: SessionDep,
    days: Annotated[
        int, Query(ge=1, le=90, description="Number of days in the future")
    ] = 7,
) -> list[TaskRead]:
    tasks = services.fetch_upcoming_tasks(session=session, days=days)
    return [TaskRead.model_validate(task) for task in tasks]


@router.post("/reschedule")
def reschedule_tasks(
    session: SessionDep,
    request: RescheduleRequest,
) -> list[TaskRead]:
    tasks = services.reschedule(session=session, request=request)
    return [TaskRead.model_validate(task) for task in tasks]
