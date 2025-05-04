"""
    Tests for endpoints from ArticleGate Web-application
"""

from fastapi.testclient import TestClient
from .app import main as articleGate

client = TestClient(articleGate.app)


def test_welcome():
    """
        Welcome-page handler test
    """
    resp = client.get("/")
    assert resp.status_code == 200

    welcome_msg = "Welcome to ArticleGate Web-app! " + \
                  "Store and retrieve information about scientific articles."
    assert resp.json() == {"ServiceInfo": welcome_msg}


def 