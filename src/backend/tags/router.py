from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from backend.tags import services
from backend.tags.schemas import TagCreate, TagRead, TagUpdate
from backend.tasks.dependencies import SessionDep
from backend.tasks.schemas import TaskRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
def list_tags(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of tags to return")
    ] = 50,
) -> list[TagRead]:
    return services.fetch_tags(session=session, offset=offset, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tag(
    session: SessionDep,
    tag_in: TagCreate,
) -> TagRead:
    return services.create_new_tag(session=session, tag_in=tag_in)


@router.get("/{tag_id}")
def get_tag(
    session: SessionDep,
    tag_id: Annotated[int, Path(ge=1, description="The ID of the tag to retrieve")],
) -> TagRead:
    return services.fetch_tag_by_id(session=session, tag_id=tag_id)


@router.patch("/{tag_id}")
def update_tag(
    session: SessionDep,
    tag_id: Annotated[int, Path(ge=1, description="The ID of the tag to update")],
    tag_in: TagUpdate,
) -> TagRead:
    return services.update_existing_tag(session=session, tag_id=tag_id, tag_in=tag_in)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    session: SessionDep,
    tag_id: Annotated[int, Path(ge=1, description="The ID of the tag to delete")],
) -> None:
    services.remove_tag(session=session, tag_id=tag_id)


@router.get("/{tag_id}/tasks")
def list_tasks_by_tag(
    session: SessionDep,
    tag_id: Annotated[int, Path(ge=1, description="The ID of the tag")],
) -> list[TaskRead]:
    tasks = services.fetch_tasks_by_tag(session=session, tag_id=tag_id)
    return [TaskRead.model_validate(task) for task in tasks]


@router.post("/{tag_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def attach_tag_to_task(
    session: SessionDep,
    tag_id: Annotated[int, Path(ge=1, description="The ID of the tag")],
    task_id: Annotated[int, Path(ge=1, description="The ID of the task")],
) -> None:
    services.assign_tag_to_task(session=session, tag_id=tag_id, task_id=task_id)


@router.delete("/{tag_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tag_from_task(
    session: SessionDep,
    tag_id: Annotated[int, Path(ge=1, description="The ID of the tag")],
    task_id: Annotated[int, Path(ge=1, description="The ID of the task")],
) -> None:
    services.detach_tag_from_task(session=session, tag_id=tag_id, task_id=task_id)
