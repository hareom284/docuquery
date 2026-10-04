"""Day 4 — API tests with TestClient.

TestClient calls the app in-process. No server, no port, no network:
it is Laravel's $this->postJson('/documents', [...]).

Run:  uv run pytest -q
"""

from fastapi.testclient import TestClient

from docuquery.api import InMemoryStore, app, get_store

client = TestClient(app)


# TEST 1 — /health answers 200 with the right body.
def test_health():
    response = client.get("/health")
    # TODO: assert response.status_code == 200
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# TEST 2 — POST creates a document: 201, an id, and the title echoed back.
def test_create_document():
    response = client.post("/documents", json={"title": "Notes", "body": "hello"})
    # TODO: assert the status code is 201
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Notes"
    assert "id" in data


# TEST 3 — an unknown id gives 404, not a crash.
def test_read_missing_document():
    response = client.get("/documents/does-not-exist")
    # TODO: assert response.status_code == 404
    assert response.status_code == 404


# TEST 4 — a bad body is rejected by FastAPI with 422, before our code runs.
def test_validation_error():
    response = client.post("/documents", json={"title": "", "body": "hello"})
    # TODO: assert response.status_code == 422       (title has min_length=1)
    assert response.status_code == 422


# TEST 5 — dependency override: swap the real store for a fresh one.
#   This is why Depends() matters. Same idea as Laravel's $this->swap(Store::class, $fake).
def test_dependency_override():
    fake_store = InMemoryStore()
    app.dependency_overrides[get_store] = lambda: fake_store
    try:
        created = client.post("/documents", json={"title": "Fake", "body": "x"}).json()
        # TODO: fetch it back with client.get(f"/documents/{created['id']}")
        #       assert the status code is 200 and the title is "Fake"
        #       then assert the document really lives in fake_store:
        #       assert fake_store.get(created["id"]) is not None
        response = client.get(f"/documents/{created['id']}")
        assert response.status_code == 200
        data = response.json()
        assert response.json()['title'] == "Fake"
        assert data["title"] == "Fake"
        assert fake_store.get(created["id"]) is not None
    finally:
        app.dependency_overrides.clear()   # always clean up, or other tests inherit the fake
