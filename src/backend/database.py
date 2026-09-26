from sqlmodel import SQLModel, create_engine

from backend.config import settings

connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    # Ensure all models are registered with SQLModel metadata
    import backend.lists.models
    import backend.tags.models
    import backend.tasks.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
