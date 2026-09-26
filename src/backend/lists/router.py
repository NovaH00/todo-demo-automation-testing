from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from backend.lists import services
from backend.lists.schemas import ListCreate, ListRead, ListUpdate
from backend.tasks.dependencies import SessionDep
from backend.tasks.schemas import TaskRead

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("/")
def list_all_lists(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of lists to return")
    ] = 20,
) -> list[ListRead]:
    return services.fetch_lists(session=session, offset=offset, limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_list(
    session: SessionDep,
    list_in: ListCreate,
) -> ListRead:
    return services.create_new_list(session=session, list_in=list_in)


@router.get("/{list_id}")
def get_list(
    session: SessionDep,
    list_id: Annotated[int, Path(ge=1, description="The ID of the list to retrieve")],
) -> ListRead:
    return services.fetch_list_by_id(session=session, list_id=list_id)


@router.patch("/{list_id}")
def update_list(
    session: SessionDep,
    list_id: Annotated[int, Path(ge=1, description="The ID of the list to update")],
    list_in: ListUpdate,
) -> ListRead:
    return services.update_existing_list(
        session=session, list_id=list_id, list_in=list_in
    )


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(
    session: SessionDep,
    list_id: Annotated[int, Path(ge=1, description="The ID of the list to delete")],
) -> None:
    services.remove_list(session=session, list_id=list_id)


@router.get("/{list_id}/tasks")
def list_tasks_in_list(
    session: SessionDep,
    list_id: Annotated[int, Path(ge=1, description="The ID of the list")],
) -> list[TaskRead]:
    tasks = services.fetch_tasks_in_list(session=session, list_id=list_id)
    return [TaskRead.model_validate(task) for task in tasks]
