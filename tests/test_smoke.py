"""Smoke test: verify the package and its key public symbols import correctly."""

from rainbowminer_api_client import (
    BinaryResponse,
    CurrentProfit,
    RainbowMinerClient,
    RainbowMinerError,
    SyncRainbowMinerClient,
)


def test_imports() -> None:
    """Verify that the main public symbols are importable and correct types."""
    assert RainbowMinerClient is not None
    assert SyncRainbowMinerClient is not None
    assert issubclass(RainbowMinerError, Exception)
    assert BinaryResponse is not None
    assert CurrentProfit is not None
