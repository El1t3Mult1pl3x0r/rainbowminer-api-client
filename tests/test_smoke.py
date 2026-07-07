"""Smoke tests for the rainbowminer_api_client package."""

from rainbowminer_api_client import hello


def test_hello() -> None:
    """Verify the hello function returns the expected greeting."""
    assert hello() == "Hello from rainbowminer-api-client!"
