from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_exercise():
    payload = {
        "name": "Push Ups",
        "difficulty": "beginner",
        "muscle_group": "chest"
    }

    response = client.post("/exercises", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Push Ups"
    assert data["difficulty"] == "beginner"
    assert data["muscle_group"] == "chest"
    assert "id" in data


def test_list_exercises():
    response = client.get("/exercises")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
