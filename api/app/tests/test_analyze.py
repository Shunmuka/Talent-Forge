"""Tests for analyze endpoint."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_with_text():
    """Test analyze endpoint with text input."""
    payload = {
        "resumeText": "Software Engineer with 5 years of experience in Python and JavaScript.",
        "jobDescription": "We are looking for a Senior Software Engineer with experience in Python, JavaScript, and React."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "gaps" in data
    assert "evidence" in data
    assert "bullets" in data
    assert isinstance(data["score"], int)
    assert 0 <= data["score"] <= 100


def test_analyze_missing_job_description():
    """Test analyze endpoint with missing job description."""
    payload = {
        "resumeText": "Software Engineer with 5 years of experience."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422  # Validation error


def test_analyze_empty_resume():
    """Test analyze endpoint with empty resume."""
    payload = {
        "resumeText": "",
        "jobDescription": "Job description text"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 400

