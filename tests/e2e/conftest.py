from collections.abc import Iterator

import httpx
import pytest
from pytest_django.live_server_helper import LiveServer


@pytest.fixture
def client(live_server: LiveServer) -> Iterator[httpx.Client]:
    with httpx.Client(base_url=live_server.url, follow_redirects=False) as http_client:
        yield http_client
