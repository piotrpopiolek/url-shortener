import pytest

from shortener.models import Link
from shortener.services import (
    CodeGenerationError,
    ShortURLNotFoundError,
    create_short_url,
    get_original_url,
    expand_short_url,
)


@pytest.mark.django_db
def test_create_short_url_persists_original_url() -> None:
    original_url = "https://example.com/very/long"
    link = create_short_url(original_url)
    assert link.url == original_url
    assert Link.objects.get(code=link.code).url == original_url

@pytest.mark.django_db
def test_create_short_url_same_url_twice_gives_different_codes() -> None:
    original_url = "https://example.com/very/long"
    link1 = create_short_url(original_url)
    link2 = create_short_url(original_url)
    assert link1.code != link2.code
    assert Link.objects.filter(url=original_url).count() == 2

@pytest.mark.django_db
def test_create_short_url_retries_on_collision() -> None:
    Link.objects.create(code="taken01", url="https://example.com/very/long")
    codes = iter(["taken01", "fresh01"])
    link = create_short_url(
        "https://example.com/very/long",
        generate=lambda: next(codes),
    )
    assert link.code == "fresh01"

@pytest.mark.django_db
def test_create_short_url_raises_error_after_max_attempts() -> None:
    Link.objects.create(code="taken01", url="https://example.com/very/long")
    with pytest.raises(CodeGenerationError):
        create_short_url(
            "https://example.com/very/long",
            generate=lambda: "taken01",
        )

@pytest.mark.django_db
def test_get_original_url_returns_url_for_known_code() -> None:
    Link.objects.create(code="known01", url="https://example.com/very/long")
    assert get_original_url("known01") == "https://example.com/very/long"

@pytest.mark.django_db
def test_get_original_url_raises_error_for_unknown_code() -> None:
    with pytest.raises(ShortURLNotFoundError):
        get_original_url("unknown01")


@pytest.mark.django_db
def test_expand_short_url_round_trip() -> None:
    original_url = "https://example.com/very/long"
    link = create_short_url(original_url)
    assert expand_short_url(f"https://sho.rt/shrt/{link.code}") == original_url