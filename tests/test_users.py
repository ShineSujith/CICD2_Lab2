# tests/test_users.py

import pytest
from app.main import users
from conftests import client #need this cause venv not working correctly

def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

def test_create_user_ok(client: client):
    """tests if you can successfully create a user"""
    result = client.post("/api/users", json=user_payload())
    assert result.status_code == 201
    data = result.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"
    users.clear() #clears global list

def test_duplicate_user_id_conflict(client: client):
    """tests you can create a user with an existing id"""
    client.post("/api/users", json=user_payload(uid=2))
    result = client.post("/api/users", json=user_payload(uid=2))
    assert result.status_code == 409 # duplicate id -> conflict
    assert "exists" in result.json()["detail"].lower()
    users.clear()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client: client, bad_sid):
    """tests invalid user ids throw 422 error"""
    result = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert result.status_code == 422 # pydantic validation error
    users.clear()

def test_get_user_404(client: client):
    """tests 404 is thrown when a user does not exist when trying to get them"""
    result = client.get("/api/users/999")
    assert result.status_code == 404
    users.clear()

def test_delete_then_404(client: client):
    """tests 404 is throw when trying to delete a user who does not exist"""
    client.post("/api/users", json=user_payload(uid=10))
    result1 = client.delete("/api/delete/users/10")
    assert result1.status_code == 204
    result2 = client.delete("/api/delete/users/10")
    assert result2.status_code == 404
    users.clear()

def test_edit_user_ok(client: client):
    """tests you can edit an existing user"""
    client.post("/api/users", json=user_payload(uid=2))
    client.post("/api/users/2", json=user_payload())
    result1 = client.put("/api/users/2", json=user_payload(age=20))
    print(result1)
    assert result1.status_code == 200
    users.clear()

def test_edit_user_404(client: client):
    """tests you can't edit a user that does not exist"""
    client.post("/api/users", json=user_payload())
    result = client.put("/api/users/2", json=user_payload(age=20))
    assert result.status_code == 404
    users.clear()

@pytest.mark.parametrize("bad_age", ["BAD", "10", "$^", "bad"])
def test_bad_age_422(client: client, bad_age):
    """tests invalid ages"""
    result = client.post("/api/users", json=user_payload(uid=3, sid=bad_age))
    assert result.status_code == 422 # pydantic validation error
    users.clear()