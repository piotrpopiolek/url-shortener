import pytest

from shortener.serializers import ShortenRequestSerializer


@pytest.mark.parametrize("url", ["http://example.com/a", "https://example.com/a"])
def test_shorten_serializer_accepts_http_and_https(url: str) -> None:
    serializer = ShortenRequestSerializer(data={"url": url})

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["url"] == url


@pytest.mark.parametrize("url", ["ftp://example.com/a", "javascript:alert(1)"])
def test_shorten_serializer_rejects_non_http_schemes(url: str) -> None:
    serializer = ShortenRequestSerializer(data={"url": url})

    assert not serializer.is_valid()


def test_shorten_serializer_rejects_url_without_scheme() -> None:
    serializer = ShortenRequestSerializer(data={"url": "example.com/a"})
    assert not serializer.is_valid()
    assert "url" in serializer.errors


def test_shorten_serializer_rejects_too_long_url() -> None:
    url = "https://example.com/" + ("a" * 2048)
    serializer = ShortenRequestSerializer(data={"url": url})

    assert not serializer.is_valid()
    assert "url" in serializer.errors


def test_shorten_serializer_rejects_missing_field() -> None:
    serializer = ShortenRequestSerializer(data={})
    assert not serializer.is_valid()
    assert "url" in serializer.errors
