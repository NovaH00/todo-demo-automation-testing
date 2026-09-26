from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_create_and_get_task(client: TestClient) -> None:
    payload = {
        "title": "Buy groceries",
        "description": "Milk, eggs, and bread",
        "priority": "high",
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["id"] is not None
    assert created_task["title"] == "Buy groceries"
    assert created_task["description"] == "Milk, eggs, and bread"
    assert created_task["priority"] == "high"
    assert created_task["is_completed"] is False

    task_id = created_task["id"]
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id


def test_list_and_filter_tasks(client: TestClient) -> None:
    client.post(
        "/tasks/",
        json={"title": "Task 1", "priority": "low", "is_completed": False},
    )
    client.post(
        "/tasks/",
        json={"title": "Task 2", "priority": "high", "is_completed": True},
    )
    client.post(
        "/tasks/",
        json={
            "title": "Special Search Task",
            "priority": "medium",
            "is_completed": False,
        },
    )

    # List all
    all_res = client.get("/tasks/")
    assert all_res.status_code == 200
    assert len(all_res.json()) >= 3

    # Filter by status completed
    completed_res = client.get("/tasks/?status=completed")
    assert completed_res.status_code == 200
    assert all(task["is_completed"] is True for task in completed_res.json())

    # Filter by status pending
    pending_res = client.get("/tasks/?status=pending")
    assert pending_res.status_code == 200
    assert all(task["is_completed"] is False for task in pending_res.json())

    # Filter by priority
    high_res = client.get("/tasks/?priority=high")
    assert high_res.status_code == 200
    assert all(task["priority"] == "high" for task in high_res.json())

    # Search
    search_res = client.get("/tasks/?search=Special")
    assert search_res.status_code == 200
    assert len(search_res.json()) == 1
    assert search_res.json()[0]["title"] == "Special Search Task"


def test_update_task(client: TestClient) -> None:
    create_res = client.post("/tasks/", json={"title": "Initial title"})
    task_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated title", "is_completed": True},
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["title"] == "Updated title"
    assert updated["is_completed"] is True


def test_delete_task(client: TestClient) -> None:
    create_res = client.post("/tasks/", json={"title": "To be deleted"})
    task_id = create_res.json()["id"]

    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204

    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404


def test_task_not_found(client: TestClient) -> None:
    res = client.get("/tasks/999999")
    assert res.status_code == 404


def test_task_validation_error(client: TestClient) -> None:
    # Empty title should fail min_length=1 validation
    res = client.post("/tasks/", json={"title": ""})
    assert res.status_code == 422
