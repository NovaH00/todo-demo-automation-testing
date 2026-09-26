from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient


def test_schedule_queries(client: TestClient) -> None:
    now = datetime.now(UTC)

    # Overdue task
    overdue_time = (now - timedelta(days=2)).isoformat()
    client.post(
        "/tasks/",
        json={"title": "Past deadline task", "due_date": overdue_time},
    )

    # Today task
    today_time = now.isoformat()
    client.post(
        "/tasks/",
        json={"title": "Due today task", "due_date": today_time},
    )

    # Upcoming task
    upcoming_time = (now + timedelta(days=3)).isoformat()
    client.post(
        "/tasks/",
        json={"title": "Future task", "due_date": upcoming_time},
    )

    # Check overdue
    overdue_res = client.get("/schedule/overdue")
    assert overdue_res.status_code == 200
    assert any(t["title"] == "Past deadline task" for t in overdue_res.json())

    # Check today
    today_res = client.get("/schedule/today")
    assert today_res.status_code == 200
    assert any(t["title"] == "Due today task" for t in today_res.json())

    # Check upcoming
    upcoming_res = client.get("/schedule/upcoming?days=5")
    assert upcoming_res.status_code == 200
    assert any(t["title"] == "Future task" for t in upcoming_res.json())

    # Check overview
    overview_res = client.get("/schedule/overview")
    assert overview_res.status_code == 200
    overview = overview_res.json()
    assert overview["overdue_count"] >= 1
    assert overview["today_count"] >= 1
    assert overview["upcoming_count"] >= 1


def test_reschedule_tasks(client: TestClient) -> None:
    task_res = client.post("/tasks/", json={"title": "To reschedule"})
    task_id = task_res.json()["id"]

    new_date = (datetime.now(UTC) + timedelta(days=10)).isoformat()
    resched_res = client.post(
        "/schedule/reschedule",
        json={"task_ids": [task_id], "new_due_date": new_date},
    )
    assert resched_res.status_code == 200
    tasks = resched_res.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["due_date"] is not None
