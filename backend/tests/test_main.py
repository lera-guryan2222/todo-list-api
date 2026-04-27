from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert "status" in response.json()