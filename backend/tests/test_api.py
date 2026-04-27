import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestTasksAPI:
    def test_create_task(self):
        client = TestClient(app)
        response = client.post(
            "/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "priority": "high",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["completed"] is False

    def test_get_tasks(self):
        client = TestClient(app)
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_task_by_id(self):
        client = TestClient(app)
        create_response = client.post("/tasks/", json={"title": "Get Test"})
        task_id = create_response.json()["id"]
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200

    def test_update_task(self):
        client = TestClient(app)
        create_response = client.post("/tasks/", json={"title": "Update Test"})
        task_id = create_response.json()["id"]
        response = client.put(f"/tasks/{task_id}", json={"completed": True})
        assert response.status_code == 200

    def test_delete_task(self):
        client = TestClient(app)
        create_response = client.post("/tasks/", json={"title": "Delete Test"})
        task_id = create_response.json()["id"]
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

    def test_get_nonexistent_task(self):
        client = TestClient(app)
        response = client.get("/tasks/99999")
        assert response.status_code == 404
        