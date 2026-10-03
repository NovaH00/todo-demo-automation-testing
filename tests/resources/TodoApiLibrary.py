from collections.abc import Generator
from typing import Any

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import backend.lists.models
import backend.tags.models
import backend.tasks.models  # noqa: F401
from backend.main import app
from backend.tasks.dependencies import get_session


class TodoApiLibrary:
    """Robot Framework keyword library for testing the Todo App API."""

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    def __init__(self) -> None:
        self.engine = None
        self.client: TestClient | None = None
        self.server_process: Any | None = None
        self.test_db_path: Any | None = None

    def start_test_server(self, port: int = 8888, host: str = "127.0.0.1") -> str:
        """Start a background FastAPI server for UI tests and wait for /health."""
        import os
        import subprocess
        import sys
        import time
        import urllib.request
        from pathlib import Path

        server_port = int(port)
        server_host = str(host)
        self.test_db_path = Path(f"./data/test_e2e_{server_port}.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()

        env = os.environ.copy()
        env["DATABASE_URL"] = f"sqlite:///{self.test_db_path.resolve()}"
        env["PYTHONPATH"] = str(Path("src").resolve())

        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            server_host,
            "--port",
            str(server_port),
            "--log-level",
            "warning",
        ]
        self.server_process = subprocess.Popen(cmd, env=env)

        base_url = f"http://{server_host}:{server_port}"
        deadline = time.time() + 10
        server_ready = False
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"{base_url}/health", timeout=1) as resp:
                    if resp.status == 200:
                        server_ready = True
                        break
            except (urllib.error.URLError, OSError):
                time.sleep(0.2)

        if not server_ready:
            self.stop_test_server()
            raise RuntimeError(f"Test server failed to start at {base_url}")

        return base_url

    def stop_test_server(self) -> None:
        """Stop the background test server and clean up test database."""
        import subprocess

        if self.server_process is not None:
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            self.server_process = None

        if self.test_db_path is not None and self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except OSError:
                pass

    def initialize_database(self) -> None:
        """Create an in-memory SQLite database and configure TestClient."""
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(self.engine)

        def get_session_override() -> Generator[Session]:
            with Session(self.engine) as session:
                yield session

        app.dependency_overrides[get_session] = get_session_override
        self.client = TestClient(app)

    def close_database(self) -> None:
        """Clean up test client and clear dependency overrides."""
        if self.client:
            self.client.close()
        app.dependency_overrides.clear()

    def _get_client(self) -> TestClient:
        if self.client is None:
            self.initialize_database()
        assert self.client is not None
        return self.client

    # System
    def check_health(self) -> dict[str, Any]:
        """Call the /health endpoint and return the JSON response."""
        res = self._get_client().get("/health")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    # Tasks
    def create_task(
        self,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        is_completed: bool = False,
        list_id: int | None = None,
        due_date: str | None = None,
        tag_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        """Create a new task via POST /tasks/."""
        payload: dict[str, Any] = {
            "title": title,
            "description": description,
            "priority": priority,
            "is_completed": is_completed,
            "list_id": int(list_id) if list_id is not None else None,
            "due_date": due_date,
            "tag_ids": [int(t) for t in tag_ids] if tag_ids else [],
        }
        res = self._get_client().post("/tasks/", json=payload)
        assert res.status_code == 201, (
            f"Expected 201, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_task(self, task_id: int) -> dict[str, Any]:
        """Get a task by ID via GET /tasks/{task_id}."""
        res = self._get_client().get(f"/tasks/{task_id}")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_nonexistent_task(self, task_id: int) -> int:
        """Verify GET /tasks/{task_id} returns 404."""
        res = self._get_client().get(f"/tasks/{task_id}")
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"
        return res.status_code

    def list_tasks(
        self,
        status: str = "all",
        priority: str | None = None,
        search: str | None = None,
        list_id: int | None = None,
        tag_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """List tasks with optional filters via GET /tasks/."""
        params: dict[str, Any] = {}
        if status != "all":
            params["status"] = status
        if priority:
            params["priority"] = priority
        if search:
            params["search"] = search
        if list_id is not None:
            params["list_id"] = int(list_id)
        if tag_id is not None:
            params["tag_id"] = int(tag_id)

        res = self._get_client().get("/tasks/", params=params)
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def update_task(self, task_id: int, **fields: Any) -> dict[str, Any]:
        """Update a task via PATCH /tasks/{task_id}."""
        payload: dict[str, Any] = {}
        for k, v in fields.items():
            if k == "list_id" and v is not None:
                payload[k] = int(v)
            elif k == "tag_ids" and v is not None:
                payload[k] = [int(x) for x in v]
            elif k == "is_completed":
                payload[k] = str(v).lower() in ("true", "1")
            else:
                payload[k] = v

        res = self._get_client().patch(f"/tasks/{task_id}", json=payload)
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def delete_task(self, task_id: int) -> None:
        """Delete a task via DELETE /tasks/{task_id}."""
        res = self._get_client().delete(f"/tasks/{task_id}")
        assert res.status_code == 204, f"Expected 204, got {res.status_code}"

    def create_task_with_invalid_data(self, **data: Any) -> int:
        """Verify POST /tasks/ with invalid data returns 422."""
        res = self._get_client().post("/tasks/", json=data)
        assert res.status_code == 422, f"Expected 422, got {res.status_code}"
        return res.status_code

    def update_nonexistent_task(self, task_id: int, **data: Any) -> int:
        """Verify PATCH /tasks/{task_id} on missing task returns 404."""
        res = self._get_client().patch(f"/tasks/{task_id}", json=data)
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"
        return res.status_code

    def delete_nonexistent_task(self, task_id: int) -> int:
        """Verify DELETE /tasks/{task_id} on missing task returns 404."""
        res = self._get_client().delete(f"/tasks/{task_id}")
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"
        return res.status_code

    # Lists
    def create_todo_list(
        self,
        name: str,
        description: str | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """Create a list via POST /lists/."""
        payload = {"name": name, "description": description, "color": color}
        res = self._get_client().post("/lists/", json=payload)
        assert res.status_code == 201, (
            f"Expected 201, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_todo_list(self, list_id: int) -> dict[str, Any]:
        """Get a list by ID via GET /lists/{list_id}."""
        res = self._get_client().get(f"/lists/{list_id}")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def list_todo_lists(self) -> list[dict[str, Any]]:
        """List all lists via GET /lists/."""
        res = self._get_client().get("/lists/")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def delete_todo_list(self, list_id: int) -> None:
        """Delete a list via DELETE /lists/{list_id}."""
        res = self._get_client().delete(f"/lists/{list_id}")
        assert res.status_code == 204, f"Expected 204, got {res.status_code}"

    def get_tasks_for_todo_list(self, list_id: int) -> list[dict[str, Any]]:
        """Get tasks attached to a list via GET /lists/{list_id}/tasks."""
        res = self._get_client().get(f"/lists/{list_id}/tasks")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    # Tags
    def create_tag(self, name: str, color: str | None = None) -> dict[str, Any]:
        """Create a tag via POST /tags/."""
        payload = {"name": name, "color": color}
        res = self._get_client().post("/tags/", json=payload)
        assert res.status_code == 201, (
            f"Expected 201, got {res.status_code}: {res.text}"
        )
        return res.json()

    def create_duplicate_tag_should_fail(self, name: str) -> int:
        """Verify creating a duplicate tag returns 409 Conflict."""
        payload = {"name": name}
        res = self._get_client().post("/tags/", json=payload)
        assert res.status_code == 409, f"Expected 409, got {res.status_code}"
        return res.status_code

    def list_all_tags(self) -> list[dict[str, Any]]:
        """List all tags via GET /tags/."""
        res = self._get_client().get("/tags/")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def attach_tag_to_task(self, tag_id: int, task_id: int) -> None:
        """Associate a tag with a task via POST /tags/{tag_id}/tasks/{task_id}."""
        res = self._get_client().post(f"/tags/{tag_id}/tasks/{task_id}")
        assert res.status_code == 204, f"Expected 204, got {res.status_code}"

    def detach_tag_from_task(self, tag_id: int, task_id: int) -> None:
        """Remove a tag from a task via DELETE /tags/{tag_id}/tasks/{task_id}."""
        res = self._get_client().delete(f"/tags/{tag_id}/tasks/{task_id}")
        assert res.status_code == 204, f"Expected 204, got {res.status_code}"

    def get_tasks_for_tag(self, tag_id: int) -> list[dict[str, Any]]:
        """Get tasks with tag via GET /tags/{tag_id}/tasks."""
        res = self._get_client().get(f"/tags/{tag_id}/tasks")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    # Schedule
    def get_schedule_overview(self) -> dict[str, Any]:
        """Fetch schedule overview via GET /schedule/overview."""
        res = self._get_client().get("/schedule/overview")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_today_tasks(self) -> list[dict[str, Any]]:
        """Fetch today's tasks via GET /schedule/today."""
        res = self._get_client().get("/schedule/today")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_overdue_tasks(self) -> list[dict[str, Any]]:
        """Fetch overdue tasks via GET /schedule/overdue."""
        res = self._get_client().get("/schedule/overdue")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_upcoming_tasks(self, days: int = 7) -> list[dict[str, Any]]:
        """Fetch upcoming tasks via GET /schedule/upcoming."""
        res = self._get_client().get(f"/schedule/upcoming?days={days}")
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def reschedule_tasks(
        self, task_ids: list[int], new_due_date: str
    ) -> list[dict[str, Any]]:
        """Batch reschedule tasks via POST /schedule/reschedule."""
        payload = {
            "task_ids": [int(tid) for tid in task_ids],
            "new_due_date": new_due_date,
        }
        res = self._get_client().post("/schedule/reschedule", json=payload)
        assert res.status_code == 200, (
            f"Expected 200, got {res.status_code}: {res.text}"
        )
        return res.json()

    def get_relative_iso_date(
        self, days_offset: int = 0, hours_offset: int = 0
    ) -> str:
        """Return an ISO formatted timestamp relative to UTC now by day and hour offset."""
        from datetime import UTC, datetime, timedelta

        target = datetime.now(UTC) + timedelta(
            days=int(days_offset), hours=int(hours_offset)
        )
        return target.isoformat()
