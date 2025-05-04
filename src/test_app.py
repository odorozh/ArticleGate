"""
    Tests for endpoints from ArticleGate Web-application
"""

from fastapi.testclient import TestClient
from .app import main as articleGate

client = TestClient(articleGate.app, raise_server_exceptions=False)


def test_welcome():
    """
        Welcome-page handler test
    """
    resp = client.get("/")
    assert resp.status_code == 200

    welcome_msg = "Welcome to ArticleGate Web-app! " + \
                  "Store and retrieve information about scientific articles."
    assert resp.json() == {"ServiceInfo": welcome_msg}


def test_get_author():
    """
        Simple GET author test
        GET /author
    """
    resp1 = client.get("/author?id=0")
    assert resp1.status_code == 200
    answer1 = {
        "affiliation_org_id": 0,
        "name": "Talal AL-Yazeedi",
        "id": 0
    }
    assert resp1.json() == answer1

    resp2 = client.get("/author")
    assert resp2.status_code == 422


def test_get_article():
    """
        Simple GET article test
        GET /article
    """
    resp1 = client.get("/article?doi=10.1101/2025.04.16.649184")
    assert resp1.status_code == 200
    assert resp1.json () == {
        "posting_date": "2025-04-22",
        "doi": "10.1101/2025.04.16.649184",
        "title": "Genetic mapping of resistance: A QTL and associated polymorphism conferring resistance to alpha-cypermethrin in Anopheles funestus"
    }

    resp2 = client.get("/article?hhh=test")
    assert resp2.status_code == 422


def test_get_org():
    """
        Simple GET organisation test
        GET /org
    """
    resp1 = client.get("/org?id=0")
    assert resp1.status_code == 200
    assert resp1.json () == {
        "title": "Liverpool School of Tropical Medicine",
        "id": 0,
        "location": "Liverpool, UK"
    }

    resp2 = client.get("/org?test=test")
    assert resp2.status_code == 422


def test_get_articles_by_author():
    """
        Simple GET articles_by_author test
        GET /articles_by_author
    """
    resp1 = client.get("/articles_by_author?id=0")
    assert resp1.status_code == 200
    assert len(resp1.json()) == 3


def test_get_authors_of_article():
    """
        Simple GET authors of article test
        GET /authors_of_article
    """
    resp1 = client.get("/authors_of_article?doi=10.1101/2025.04.16.649184")
    assert resp1.status_code == 200
    assert len(resp1.json()) == 6


def test_auth():
    """
        Auth admin test
    """
    data = {
        "grant_type": "password",
        "username": "veritas",
        "password": "testpass",
        "client_id": "string",
        "client_secret": "string"
    }
    resp = client.post("/auth", data=data)
    assert resp.status_code == 401


def test_create_article():
    """
        Test POST /create/author
    """
    data = {
        "id": "-8",
        "name": "testAuthor",
        "affiliation_org_id": "0"
    }
    resp = client.post("/create/author", data=data)
    assert resp.status_code == 500


def test_create_article():
    """
        Test POST /create/article
    """
    data = {
        "doi": "test_doi",
        "title": "testTitle",
        "posting_data": "2025-08-09"
    }
    resp = client.post("/create/article", data=data)
    assert resp.status_code == 500


def test_create_article_to_author():
    """
        Test POST /create/article_to_author
    """
    data = {
        "doi": "128",
        "author_id": "1",
        "place": "1"
    }
    resp = client.post("/create/article_to_author", data=data)
    assert resp.status_code == 500


def test_create_org():
    """
        Test POST /create/org
    """
    data = {
        "id": "128",
        "title": "testTitle",
        "location": "town"
    }
    resp = client.post("/create/org", data=data)
    assert resp.status_code == 500
