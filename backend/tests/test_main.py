from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app


class TestMain:
    def setup_method(self):
        Base.metadata.create_all(bind=engine)

    def teardown_method(self):
        Base.metadata.drop_all(bind=engine)

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