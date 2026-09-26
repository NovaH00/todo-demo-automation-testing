from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from backend.tasks import services
from backend.tasks.constants import TaskPriority, TaskStatusFilter
from backend.tasks.dependencies import SessionDep
from backend.tasks.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
def list_tasks(
    session: SessionDep,
    status_filter: Annotated[
        TaskStatusFilter,
        Query(
            alias="status",
            description="Filter tasks by completion status",
        ),
    ] = TaskStatusFilter.ALL,
    priority: Annotated[
        TaskPriority | None,
        Query(description="Filter tasks by priority"),
    ] = None,
    search: Annotated[
        str | None,
        Query(description="Search term in title or description"),
    ] = None,
    list_id: Annotated[
        int | None,
        Query(description="Filter tasks by list ID"),
    ] = None,
    tag_id: Annotated[
        int | None,
        Query(description="Filter tasks by tag ID"),
    ] = None,
    offset: Annotated[
        int,
        Query(ge=0, description="Offset for pagination"),
    ] = 0,
    limit: Annotated[
        int,
        Query(ge=1, le=100, description="Maximum number of tasks to return"),
    ] = 20,
) -> list[TaskRead]:
    return services.fetch_tasks(
        session=session,
        status_filter=status_filter,
        priority=priority,
        search=search,
        list_id=list_id,
        tag_id=tag_id,
        offset=offset,
        limit=limit,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(
    session: SessionDep,
    task_in: TaskCreate,
) -> TaskRead:
    return services.create_new_task(session=session, task_in=task_in)


@router.get("/{task_id}")
def get_task(
    session: SessionDep,
    task_id: Annotated[int, Path(ge=1, description="The ID of the task to retrieve")],
) -> TaskRead:
    return services.fetch_task_by_id(session=session, task_id=task_id)


@router.patch("/{task_id}")
def update_task(
    session: SessionDep,
    task_id: Annotated[int, Path(ge=1, description="The ID of the task to update")],
    task_in: TaskUpdate,
) -> TaskRead:
    return services.update_existing_task(
        session=session,
        task_id=task_id,
        task_in=task_in,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    session: SessionDep,
    task_id: Annotated[int, Path(ge=1, description="The ID of the task to delete")],
) -> None:
    services.remove_task(session=session, task_id=task_id)
