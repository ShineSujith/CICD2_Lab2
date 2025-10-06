#tests/conftest.py

from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    """Creates a new instance of app for each test"""
    return TestClient(app)
