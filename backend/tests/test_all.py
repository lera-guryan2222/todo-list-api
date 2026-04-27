import pytest
from app import crud, schemas
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestTasksAPI:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_check(self):
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["database"] == "connected"

    def test_create_task(self):
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
        assert "id" in data

    def test_get_tasks(self):
        client.post("/tasks/", json={"title": "Task 1"})
        client.post("/tasks/", json={"title": "Task 2"})
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2

    def test_get_task_by_id(self):
        create_response = client.post("/tasks/", json={"title": "Get Test"})
        task_id = create_response.json()["id"]
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Get Test"

    def test_update_task(self):
        create_response = client.post("/tasks/", json={"title": "Update Test"})
        task_id = create_response.json()["id"]
        response = client.put(f"/tasks/{task_id}", json={"completed": True})
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_delete_task(self):
        create_response = client.post("/tasks/", json={"title": "Delete Test"})
        task_id = create_response.json()["id"]
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_get_nonexistent_task(self):
        response = client.get("/tasks/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Задача не найдена"


class TestCRUD:
    def test_create_task(self, db_session):
        task_data = schemas.TaskCreate(
            title="Test CRUD Task",
            description="CRUD Test",
            priority="high"
        )
        task = crud.TaskCRUD.create_task(db_session, task_data)
        assert task.id is not None
        assert task.title == "Test CRUD Task"
        assert task.priority == "high"

    def test_get_task(self, db_session):
        task_data = schemas.TaskCreate(title="Get CRUD Task")
        created = crud.TaskCRUD.create_task(db_session, task_data)
        fetched = crud.TaskCRUD.get_task(db_session, created.id)
        assert fetched.title == "Get CRUD Task"

    def test_get_tasks(self, db_session):
        crud.TaskCRUD.create_task(db_session, schemas.TaskCreate(title="Task 1"))
        crud.TaskCRUD.create_task(db_session, schemas.TaskCreate(title="Task 2"))
        tasks = crud.TaskCRUD.get_tasks(db_session)
        assert len(tasks) >= 2

    def test_update_task(self, db_session):
        created = crud.TaskCRUD.create_task(
            db_session,
            schemas.TaskCreate(title="Original")
        )
        update_data = schemas.TaskUpdate(title="Updated", completed=True)
        updated = crud.TaskCRUD.update_task(db_session, created.id, update_data)
        assert updated.title == "Updated"
        assert updated.completed is True

    def test_delete_task(self, db_session):
        created = crud.TaskCRUD.create_task(
            db_session,
            schemas.TaskCreate(title="To Delete")
        )
        result = crud.TaskCRUD.delete_task(db_session, created.id)
        assert result is True
        deleted = crud.TaskCRUD.get_task(db_session, created.id)
        assert deleted is None

    def test_delete_nonexistent_task(self, db_session):
        result = crud.TaskCRUD.delete_task(db_session, 99999)
        assert result is False
