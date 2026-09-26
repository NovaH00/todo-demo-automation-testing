from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import create_db_and_tables
from backend.lists.router import router as lists_router
from backend.schedule.router import router as schedule_router
from backend.tags.router import router as tags_router
from backend.tasks.router import router as tasks_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(tasks_router)
app.include_router(lists_router)
app.include_router(tags_router)
app.include_router(schedule_router)


@app.get("/health", tags=["system"])
def check_health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


# Serve built Next.js static output if present
frontend_dir = Path(__file__).resolve().parent.parent / "frontend" / "out"
if frontend_dir.exists():
    app.frontend("/", directory=frontend_dir)


def main() -> None:
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )


if __name__ == "__main__":
    main()
