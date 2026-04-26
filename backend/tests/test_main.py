import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["TESTING"] = "True"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Todo List API" in response.json()["message"]


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert "status" in response.json()