import json

from app.main import app

from fastapi.testclient import TestClient


client = TestClient(app)


def test_visited_links_get():
    response = client.get("/visited_links")
    assert response.status_code == 405


def test_visited_links_post_bad():
    fake_data = [
        {},
        {"xxx": 1},
        "",
        777,
        [45, "string"],
        "string",
        {"links": 777},
        {"links": "string"},
        {"links": [777, "http://yandex.ru", "https:google.com/76"]},
        {"links": ["http://yandex.ru", "https:google.com/76"]},
    ]
    for test in fake_data:
        response = client.post("/visited_links", json=json.dumps(test))
        assert response.status_code == 400


def test_visited_domains_post():
    response = client.post("/visited_domains")
    assert response.status_code == 405


def test_visited_domains_get_bad():
    fake_data = [
        {},
        {"xxx": 1},
        "",
        "string",
        {"datetime_from": "210101000"},
        {"datetime_from": 777, "datetime_to": "String"},
        {"datetime_from": "", "datetime_to": "210101000"},
        {"datetime_from": 210101000, "datetime_to": "210201000"},
    ]
    for test in fake_data:
        response = client.get("/visited_domains", params=json.dumps(test))
        assert response.status_code == 400
