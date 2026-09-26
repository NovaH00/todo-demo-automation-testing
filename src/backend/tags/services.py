from fastapi import HTTPException, status
from sqlmodel import Session

from backend.tags import repository
from backend.tags.schemas import TagCreate, TagRead, TagUpdate
from backend.tasks.models import Task


def fetch_tags(session: Session, offset: int = 0, limit: int = 50) -> list[TagRead]:
    tags = repository.list_tags(session=session, offset=offset, limit=limit)
    return [TagRead.model_validate(tag) for tag in tags]


def fetch_tag_by_id(session: Session, tag_id: int) -> TagRead:
    tag = repository.get_tag_by_id(session, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with ID {tag_id} not found",
        )
    return TagRead.model_validate(tag)


def create_new_tag(session: Session, tag_in: TagCreate) -> TagRead:
    existing = repository.get_tag_by_name(session, tag_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tag '{tag_in.name}' already exists",
        )
    created = repository.create_tag(session, tag_in)
    return TagRead.model_validate(created)


def update_existing_tag(session: Session, tag_id: int, tag_in: TagUpdate) -> TagRead:
    tag = repository.get_tag_by_id(session, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with ID {tag_id} not found",
        )
    if tag_in.name and tag_in.name != tag.name:
        existing = repository.get_tag_by_name(session, tag_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tag '{tag_in.name}' already exists",
            )
    updated = repository.update_tag(session, tag, tag_in)
    return TagRead.model_validate(updated)


def remove_tag(session: Session, tag_id: int) -> None:
    tag = repository.get_tag_by_id(session, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with ID {tag_id} not found",
        )
    repository.delete_tag(session, tag)


def fetch_tasks_by_tag(session: Session, tag_id: int) -> list[Task]:
    fetch_tag_by_id(session, tag_id)
    return repository.get_tasks_for_tag(session, tag_id)


def assign_tag_to_task(session: Session, tag_id: int, task_id: int) -> None:
    fetch_tag_by_id(session, tag_id)
    repository.add_tag_to_task(session, task_id=task_id, tag_id=tag_id)


def detach_tag_from_task(session: Session, tag_id: int, task_id: int) -> None:
    repository.remove_tag_from_task(session, task_id=task_id, tag_id=tag_id)
