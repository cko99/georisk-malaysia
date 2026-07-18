"""
tests/conftest.py

Shared pytest fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Returns a FastAPI TestClient bound to the application instance."""
    return TestClient(app)
