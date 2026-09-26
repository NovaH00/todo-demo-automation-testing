from fastapi import HTTPException, status
from sqlmodel import Session

from backend.lists import repository
from backend.lists.models import TodoList
from backend.lists.schemas import ListCreate, ListRead, ListUpdate
from backend.tasks.models import Task


def to_list_read(session: Session, list_obj: TodoList) -> ListRead:
    count = 0
    if list_obj.id is not None:
        count = repository.get_task_count_for_list(session, list_obj.id)
    return ListRead(
        id=list_obj.id or 0,
        name=list_obj.name,
        description=list_obj.description,
        color=list_obj.color,
        task_count=count,
        created_at=list_obj.created_at,
        updated_at=list_obj.updated_at,
    )


def fetch_lists(
    session: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[ListRead]:
    lists = repository.list_all(session=session, offset=offset, limit=limit)
    return [to_list_read(session, item) for item in lists]


def fetch_list_by_id(session: Session, list_id: int) -> ListRead:
    list_obj = repository.get_list_by_id(session, list_id)
    if list_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found",
        )
    return to_list_read(session, list_obj)


def create_new_list(session: Session, list_in: ListCreate) -> ListRead:
    created = repository.create_list(session, list_in)
    return to_list_read(session, created)


def update_existing_list(
    session: Session, list_id: int, list_in: ListUpdate
) -> ListRead:
    list_obj = repository.get_list_by_id(session, list_id)
    if list_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found",
        )
    updated = repository.update_list(session, list_obj, list_in)
    return to_list_read(session, updated)


def remove_list(session: Session, list_id: int) -> None:
    list_obj = repository.get_list_by_id(session, list_id)
    if list_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {list_id} not found",
        )
    repository.delete_list(session, list_obj)


def fetch_tasks_in_list(session: Session, list_id: int) -> list[Task]:
    fetch_list_by_id(session, list_id)
    return repository.get_tasks_in_list(session, list_id)
