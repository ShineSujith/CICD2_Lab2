#tests/test_health.py

from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    result = client.get("/api/health")
    assert result.status_code == 200
    assert result.json() == ["status : ok"]
