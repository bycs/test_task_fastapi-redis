from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_visited_links_get():
    response = client.get("/visited_links")
    assert response.status_code == 404


def test_visited_links_post():
    fake_data = [
        {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
            ]
        },
    ]
    for test in fake_data:
        response = client.post("/visited_links", json=test)
        assert response.status_code == 200


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
        response = client.post("/visited_links", json=test)
        assert response.status_code == 404 or 200


def test_visited_domains_post():
    response = client.post("/visited_domains")
    assert response.status_code == 404


def test_visited_domains_get():
    fake_data = [
        {"datetime_from": "777", "datetime_to": "210101000"},
        {"datetime_from": "210101000", "datetime_to": "210201000"},
    ]
    for test in fake_data:
        response = client.get("/visited_domains", params=test)
        assert response.status_code == 404 or 200


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
        response = client.get("/visited_domains", params=test)
        assert response.status_code == 404
