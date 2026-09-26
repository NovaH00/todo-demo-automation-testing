from fastapi.testclient import TestClient


def test_create_and_get_list(client: TestClient) -> None:
    payload = {"name": "Groceries", "color": "#00FF00"}
    res = client.post("/lists/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Groceries"
    assert data["color"] == "#00FF00"
    assert data["task_count"] == 0
    list_id = data["id"]

    get_res = client.get(f"/lists/{list_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Groceries"


def test_list_tasks_in_list(client: TestClient) -> None:
    list_res = client.post("/lists/", json={"name": "Work"})
    list_id = list_res.json()["id"]

    # Create task attached to this list
    client.post(
        "/tasks/",
        json={"title": "Prepare report", "list_id": list_id},
    )
    # Create task not in this list
    client.post("/tasks/", json={"title": "Personal chore"})

    # Check tasks endpoint on list
    tasks_res = client.get(f"/lists/{list_id}/tasks")
    assert tasks_res.status_code == 200
    tasks = tasks_res.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Prepare report"

    # Check updated task_count on list
    list_check = client.get(f"/lists/{list_id}")
    assert list_check.json()["task_count"] == 1


def test_update_and_delete_list(client: TestClient) -> None:
    res = client.post("/lists/", json={"name": "Temporary"})
    list_id = res.json()["id"]

    patch_res = client.patch(f"/lists/{list_id}", json={"name": "Renamed"})
    assert patch_res.status_code == 200
    assert patch_res.json()["name"] == "Renamed"

    del_res = client.delete(f"/lists/{list_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/lists/{list_id}")
    assert get_res.status_code == 404
