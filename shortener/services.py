from collections.abc import Callable
from typing import Final
from urllib.parse import urlsplit

from django.db import IntegrityError, transaction

from shortener.codes import generate_code, is_valid_code
from shortener.models import Link


class ShortenerError(Exception):
    pass


class CodeGenerationError(ShortenerError):
    pass


class InvalidShortURLError(ShortenerError):
    pass


class ShortURLNotFoundError(ShortenerError):
    pass


SHORT_PATH_PREFIX: Final[str] = "/shrt/"
MAX_ATTEMPTS: Final[int] = 5


def create_short_url(
    original_url: str,
    *,
    generate: Callable[[], str] = generate_code,
    max_attempts: int = MAX_ATTEMPTS,
) -> Link:
    """Create a new short URL for the given original URL."""
    for _ in range(max_attempts):
        try:
            with transaction.atomic():
                return Link.objects.create(code=generate(), url=original_url)
        except IntegrityError:
            continue
    raise CodeGenerationError


def get_original_url(code: str) -> str:
    """Get the original URL for the given code."""
    try:
        link = Link.objects.get(code=code)
    except Link.DoesNotExist:
        raise ShortURLNotFoundError from None
    return link.url


def extract_code(short_url: str) -> str:
    """Extract the code from the given short URL."""
    path = urlsplit(short_url).path
    if not path.startswith(SHORT_PATH_PREFIX):
        raise InvalidShortURLError
    code = path.removeprefix(SHORT_PATH_PREFIX)
    if not is_valid_code(code):
        raise InvalidShortURLError
    return code


def expand_short_url(short_url: str) -> str:
    """Expand the given short URL to the original URL."""
    return get_original_url(extract_code(short_url))
