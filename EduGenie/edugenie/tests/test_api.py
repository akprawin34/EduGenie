import os

os.environ["DEMO_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qna():
    response = client.get("/api/qna", params={"question": "What is photosynthesis?"})
    assert response.status_code == 200
    assert "answer" in response.json()


def test_explain():
    response = client.post("/api/explain", json={"topic": "Photosynthesis"})
    assert response.status_code == 200
    assert response.json()["topic"] == "Photosynthesis"


def test_summary():
    response = client.post("/api/summarize", json={"text": "The Earth orbits the Sun."})
    assert response.status_code == 200
    assert "summary" in response.json()


def test_quiz_shape():
    response = client.post("/api/quiz", json={"text": "The Pythagorean theorem relates the sides of a right triangle."})
    assert response.status_code == 200
    quiz = response.json()["quiz"]
    assert len(quiz) == 3
    assert all(len(item["options"]) == 4 for item in quiz)
    assert all(item["answer"] in item["options"] for item in quiz)


def test_learning_path():
    response = client.post("/api/learning-path", json={"topic": "SQL"})
    assert response.status_code == 200
    assert "recommendations" in response.json()
