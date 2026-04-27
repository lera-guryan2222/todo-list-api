import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestMain:
    def test_root(self):
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_check(self):
        client = TestClient(app)
        response = client.get("/health/")
        assert response.status_code == 200
        assert "status" in response.json()