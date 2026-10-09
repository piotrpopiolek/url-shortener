import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_shorten_then_expand_returns_original_url(client: httpx.Client) -> None:
    original = "http://example.com/very-very/long/url/even-longer"
    created = client.post("/api/shorten/", json={"url": original})

    assert created.status_code == 201
    short_url = created.json()["short_url"]

    expanded = client.post("/api/expand/", json={"short_url": short_url})

    assert expanded.status_code == 200
    assert expanded.json()["url"] == original


def test_short_url_redirects_to_original(client: httpx.Client) -> None:
    original = "http://example.com/very-very/long/url/even-longer"
    created = client.post("/api/shorten/", json={"url": original})
    code = created.json()["code"]

    response = client.get(f"/shrt/{code}")

    assert response.status_code == 302
    assert response.headers["location"] == original


def test_short_url_from_response_is_usable_directly(client: httpx.Client) -> None:
    original = "http://example.com/very-very/long/url/even-longer"
    created = client.post("/api/shorten/", json={"url": original})
    short_url = created.json()["short_url"]

    response = client.get(short_url)

    assert response.status_code == 302
    assert response.headers["location"] == original


def test_shorten_rejects_invalid_url(client: httpx.Client) -> None:
    response = client.post("/api/shorten/", json={"url": "ftp://example.com/a"})

    assert response.status_code == 400
    assert "url" in response.json()


def test_expand_unknown_code_returns_404(client: httpx.Client) -> None:
    response = client.post(
        "/api/expand/",
        json={"short_url": "http://127.0.0.1/shrt/unknown"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found."


def test_redirect_unknown_code_returns_404(client: httpx.Client) -> None:
    response = client.get("/shrt/unknown")

    assert response.status_code == 404
