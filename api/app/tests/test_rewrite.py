"""Tests for rewrite endpoint."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rewrite_bullet():
    """Test rewrite endpoint."""
    payload = {
        "original": "Worked on software projects",
        "context": "Job description for Senior Software Engineer"
    }
    response = client.post("/api/rewrite", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "original" in data
    assert "revised" in data
    assert "rationale" in data


def test_rewrite_missing_original():
    """Test rewrite endpoint with missing original."""
    payload = {
        "context": "Job description"
    }
    response = client.post("/api/rewrite", json=payload)
    assert response.status_code == 422  # Validation error

