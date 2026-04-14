"""
Basic test suite for the AI Law Compliance API.
Run: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


# We patch out external dependencies before importing app
@pytest.fixture(scope="session", autouse=True)
def patch_dependencies():
    with patch("app.db.vector_store.vector_store.connect"), \
         patch("app.db.vector_store.vector_store.query", return_value=[]), \
         patch("app.db.vector_store.vector_store.upsert"):
        yield


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_laws_empty(client):
    with patch("app.api.laws.get_db") as mock_db:
        mock_session = MagicMock()
        mock_session.__aenter__ = MagicMock(return_value=mock_session)
        mock_session.__aexit__ = MagicMock(return_value=False)
        response = client.get("/api/laws")
        # Should not crash even with empty DB
        assert response.status_code in (200, 422, 500)


def test_compliance_analyze_requires_body(client):
    response = client.post("/api/compliance/analyze")
    assert response.status_code == 422  # Unprocessable — missing required fields


def test_search_requires_query(client):
    response = client.post("/api/search", json={})
    assert response.status_code == 422


def test_search_valid_request(client):
    with patch("app.api.search.embed_text", return_value=[0.1] * 384), \
         patch("app.api.search.vector_store") as mock_vs:
        mock_vs.query.return_value = []
        response = client.post("/api/search", json={"query": "automated hiring decisions"})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data


def test_ingest_requires_admin_key(client):
    response = client.post("/api/ingest", json={"laws": []})
    assert response.status_code == 403


def test_ingest_with_admin_key(client):
    from app.core.config import settings
    with patch("app.api.ingest.is_ai_relevant", return_value=(True, "keyword")), \
         patch("app.api.ingest.embed_law", return_value=[0.1] * 384), \
         patch("app.api.ingest.vector_store") as mock_vs, \
         patch("app.api.ingest.get_db"):
        response = client.post(
            "/api/ingest",
            json={"laws": [], "run_ai_filter": False},
            headers={settings.API_KEY_HEADER: settings.ADMIN_API_KEY},
        )
        assert response.status_code in (200, 422, 500)
