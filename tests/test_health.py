#tests/test_health.py

def test_health(client):
    """tests health endpoint returns correct dict and status code on success"""
    result = client.get("/api/health")
    assert result.status_code == 200
    assert result.json() == {"status" : "ok"}
