from sqlmodel import Session, col, select

from backend.tags.models import Tag, TaskTagLink
from backend.tags.schemas import TagCreate, TagUpdate
from backend.tasks.models import Task


def get_tag_by_id(session: Session, tag_id: int) -> Tag | None:
    return session.get(Tag, tag_id)


def get_tag_by_name(session: Session, name: str) -> Tag | None:
    statement = select(Tag).where(col(Tag.name) == name)
    return session.exec(statement).first()


def list_tags(session: Session, offset: int = 0, limit: int = 50) -> list[Tag]:
    statement = select(Tag).order_by(col(Tag.name).asc()).offset(offset).limit(limit)
    return list(session.exec(statement).all())


def create_tag(session: Session, tag_in: TagCreate) -> Tag:
    tag = Tag.model_validate(tag_in)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def update_tag(session: Session, tag: Tag, tag_in: TagUpdate) -> Tag:
    tag_data = tag_in.model_dump(exclude_unset=True)
    for key, value in task_data if (task_data := tag_data) else []:
        setattr(tag, key, value)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def delete_tag(session: Session, tag: Tag) -> None:
    session.delete(tag)
    session.commit()


def get_tasks_for_tag(session: Session, tag_id: int) -> list[Task]:
    statement = (
        select(Task)
        .join(TaskTagLink, col(Task.id) == col(TaskTagLink.task_id))
        .where(col(TaskTagLink.tag_id) == tag_id)
        .order_by(col(Task.id).desc())
    )
    return list(session.exec(statement).all())


def get_tags_for_task(session: Session, task_id: int) -> list[Tag]:
    statement = (
        select(Tag)
        .join(TaskTagLink, col(Tag.id) == col(TaskTagLink.tag_id))
        .where(col(TaskTagLink.task_id) == task_id)
        .order_by(col(Tag.name).asc())
    )
    return list(session.exec(statement).all())


def get_tag_ids_for_task(session: Session, task_id: int) -> list[int]:
    statement = select(TaskTagLink.tag_id).where(col(TaskTagLink.task_id) == task_id)
    return list(session.exec(statement).all())


def add_tag_to_task(session: Session, task_id: int, tag_id: int) -> None:
    link = session.get(TaskTagLink, (task_id, tag_id))
    if not link:
        new_link = TaskTagLink(task_id=task_id, tag_id=tag_id)
        session.add(new_link)
        session.commit()


def remove_tag_from_task(session: Session, task_id: int, tag_id: int) -> None:
    link = session.get(TaskTagLink, (task_id, tag_id))
    if link:
        session.delete(link)
        session.commit()


def set_task_tags(session: Session, task_id: int, tag_ids: list[int]) -> None:
    existing_links = session.exec(
        select(TaskTagLink).where(col(TaskTagLink.task_id) == task_id)
    ).all()
    for link in existing_links:
        session.delete(link)

    for tag_id in tag_ids:
        session.add(TaskTagLink(task_id=task_id, tag_id=tag_id))
    session.commit()
