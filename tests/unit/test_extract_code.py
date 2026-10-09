import pytest

from shortener.services import InvalidShortURLError, extract_code


def test_extract_code_returns_code_from_valid_short_url() -> None:
    short_url = "https://example.com/shrt/1234567"
    code = extract_code(short_url)
    assert code == "1234567"


def test_extract_code_ignores_host() -> None:
    short_url = "https://sho.rt/shrt/aB3xY9z"
    code = extract_code(short_url)
    assert code == "aB3xY9z"


def test_extract_code_rejects_wrong_path_prefix() -> None:
    with pytest.raises(InvalidShortURLError):
        extract_code("https://example.com/api/1234567")


def test_extract_code_rejects_invalid_code() -> None:
    with pytest.raises(InvalidShortURLError):
        extract_code("https://example.com/shrt/12-4-67")


def test_extract_code_rejects_empty_code() -> None:
    with pytest.raises(InvalidShortURLError):
        extract_code("https://example.com/shrt/")
