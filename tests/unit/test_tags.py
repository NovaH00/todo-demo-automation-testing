from fastapi.testclient import TestClient


def test_create_and_get_tag(client: TestClient) -> None:
    res = client.post("/tags/", json={"name": "urgent", "color": "#FF0000"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "urgent"
    assert data["color"] == "#FF0000"
    tag_id = data["id"]

    get_res = client.get(f"/tags/{tag_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == tag_id


def test_tag_duplicate_name_error(client: TestClient) -> None:
    client.post("/tags/", json={"name": "duplicate-tag"})
    dup_res = client.post("/tags/", json={"name": "duplicate-tag"})
    assert dup_res.status_code == 409


def test_task_tag_association(client: TestClient) -> None:
    tag_res = client.post("/tags/", json={"name": "work"})
    tag_id = tag_res.json()["id"]

    task_res = client.post(
        "/tasks/", json={"title": "Client meeting", "tag_ids": [tag_id]}
    )
    assert task_res.status_code == 201
    task_data = task_res.json()
    assert tag_id in task_data["tag_ids"]

    # Check tasks by tag
    tag_tasks = client.get(f"/tags/{tag_id}/tasks")
    assert tag_tasks.status_code == 200
    assert len(tag_tasks.json()) == 1

    # Remove tag from task
    task_id = task_data["id"]
    del_link = client.delete(f"/tags/{tag_id}/tasks/{task_id}")
    assert del_link.status_code == 204

    # Verify link removed
    tag_tasks_after = client.get(f"/tags/{tag_id}/tasks")
    assert len(tag_tasks_after.json()) == 0
