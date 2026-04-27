from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class TestCRUD:
    def setup_method(self):
        Base.metadata.create_all(bind=engine)

    def teardown_method(self):
        Base.metadata.drop_all(bind=engine)

    def test_create_task(self):
        db = TestingSessionLocal()
        task_data = schemas.TaskCreate(
            title="Test CRUD Task",
            description="CRUD Test",
            priority="high"
        )
        task = crud.TaskCRUD.create_task(db, task_data)
        assert task.id is not None
        assert task.title == "Test CRUD Task"
        db.close()

    def test_get_task(self):
        db = TestingSessionLocal()
        task_data = schemas.TaskCreate(title="Get CRUD Task")
        created = crud.TaskCRUD.create_task(db, task_data)
        fetched = crud.TaskCRUD.get_task(db, created.id)
        assert fetched.title == "Get CRUD Task"
        db.close()

    def test_get_tasks(self):
        db = TestingSessionLocal()
        crud.TaskCRUD.create_task(db, schemas.TaskCreate(title="Task 1"))
        crud.TaskCRUD.create_task(db, schemas.TaskCreate(title="Task 2"))
        tasks = crud.TaskCRUD.get_tasks(db)
        assert len(tasks) >= 2
        db.close()

    def test_update_task(self):
        db = TestingSessionLocal()
        created = crud.TaskCRUD.create_task(db, schemas.TaskCreate(title="Original"))
        update_data = schemas.TaskUpdate(title="Updated", completed=True)
        updated = crud.TaskCRUD.update_task(db, created.id, update_data)
        assert updated.title == "Updated"
        assert updated.completed is True
        db.close()

    def test_delete_task(self):
        db = TestingSessionLocal()
        created = crud.TaskCRUD.create_task(db, schemas.TaskCreate(title="To Delete"))
        result = crud.TaskCRUD.delete_task(db, created.id)
        assert result is True
        deleted = crud.TaskCRUD.get_task(db, created.id)
        assert deleted is None
        db.close()