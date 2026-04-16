def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "OK"}


def test_create_todo(client):
    res = client.post("/todos", json={
        "title": "테스트 할 일",
        "description": "pytest로 생성",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "테스트 할 일"
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_empty_title_rejected(client):
    res = client.post("/todos", json={"title": ""})
    assert res.status_code == 422


def test_list_todos_empty(client):
    res = client.get("/todos")
    assert res.status_code == 200
    assert res.json() == []


def test_list_todos_after_create(client):
    client.post("/todos", json={"title": "할 일 1"})
    client.post("/todos", json={"title": "할 일 2"})
    res = client.get("/todos")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_todo_by_id(client):
    create_res = client.post("/todos", json={"title": "조회 테스트"})
    todo_id = create_res.json()["id"]

    res = client.get(f"/todos/{todo_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "조회 테스트"


def test_get_todo_not_found(client):
    res = client.get("/todos/9999")
    assert res.status_code == 404


def test_update_todo(client):
    create_res = client.post("/todos", json={"title": "수정 전"})
    todo_id = create_res.json()["id"]

    res = client.patch(f"/todos/{todo_id}", json={
        "title": "수정 후",
        "completed": True,
    })
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "수정 후"
    assert data["completed"] is True


def test_update_todo_partial(client):
    create_res = client.post("/todos", json={
        "title": "부분 수정",
        "description": "원래 설명",
    })
    todo_id = create_res.json()["id"]

    res = client.patch(f"/todos/{todo_id}", json={"completed": True})
    data = res.json()
    assert data["title"] == "부분 수정"
    assert data["description"] == "원래 설명"
    assert data["completed"] is True


def test_delete_todo(client):
    create_res = client.post("/todos", json={"title": "삭제 대상"})
    todo_id = create_res.json()["id"]

    res = client.delete(f"/todos/{todo_id}")
    assert res.status_code == 204

    res = client.get(f"/todos/{todo_id}")
    assert res.status_code == 404


def test_delete_todo_not_found(client):
    res = client.delete("/todos/9999")
    assert res.status_code == 404