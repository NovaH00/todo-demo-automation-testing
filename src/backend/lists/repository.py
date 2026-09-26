from datetime import UTC, datetime

from sqlmodel import Session, col, func, select

from backend.lists.models import TodoList
from backend.lists.schemas import ListCreate, ListUpdate
from backend.tasks.models import Task


def get_list_by_id(session: Session, list_id: int) -> TodoList | None:
    return session.get(TodoList, list_id)


def list_all(session: Session, offset: int = 0, limit: int = 20) -> list[TodoList]:
    statement = (
        select(TodoList).order_by(col(TodoList.name).asc()).offset(offset).limit(limit)
    )
    return list(session.exec(statement).all())


def get_task_count_for_list(session: Session, list_id: int) -> int:
    statement = (
        select(func.count()).select_from(Task).where(col(Task.list_id) == list_id)
    )
    result = session.exec(statement).one()
    return int(result)


def create_list(session: Session, list_in: ListCreate) -> TodoList:
    list_obj = TodoList.model_validate(list_in)
    session.add(list_obj)
    session.commit()
    session.refresh(list_obj)
    return list_obj


def update_list(session: Session, list_obj: TodoList, list_in: ListUpdate) -> TodoList:
    list_data = list_in.model_dump(exclude_unset=True)
    for key, value in list_data.items():
        setattr(list_obj, key, value)
    list_obj.updated_at = datetime.now(UTC)
    session.add(list_obj)
    session.commit()
    session.refresh(list_obj)
    return list_obj


def delete_list(session: Session, list_obj: TodoList) -> None:
    session.delete(list_obj)
    session.commit()


def get_tasks_in_list(session: Session, list_id: int) -> list[Task]:
    statement = (
        select(Task).where(col(Task.list_id) == list_id).order_by(col(Task.id).desc())
    )
    return list(session.exec(statement).all())
