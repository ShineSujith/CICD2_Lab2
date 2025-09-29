#tests/test_health.py

from conftests import client

def test_health(client: client):
    result = client.get("/api/health")
    assert result.status_code == 200
    assert result.json() == {"status" : "ok"}
