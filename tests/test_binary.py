"""Tests for binary endpoints (ZIP/CSV)."""

from __future__ import annotations

from typing import Any

from rainbowminer_api_client._http import BinaryResponse


class TestCSVEndpoints:
    """Tests for CSV-returning endpoints."""

    async def test_get_totals_csv(self, client: Any) -> None:
        """get_totals_csv should return a BinaryResponse with CSV data."""
        result = await client.get_totals_csv()
        assert isinstance(result, BinaryResponse)
        assert result.content_type == "text/csv"
        assert b"Pool" in result.data
        assert result.filename is not None
        assert result.filename.endswith(".txt")

    async def test_get_earnings_csv(self, client: Any) -> None:
        """get_earnings_csv should return a BinaryResponse with CSV data."""
        result = await client.get_earnings_csv()
        assert isinstance(result, BinaryResponse)
        assert result.content_type == "text/csv"

    async def test_get_balances_csv(self, client: Any) -> None:
        """get_balances(as_csv=True) should return a BinaryResponse."""
        result = await client.get_balances(as_csv=True)
        assert isinstance(result, BinaryResponse)
        assert result.content_type == "text/csv"

    async def test_get_activity_csv(self, client: Any) -> None:
        """get_activity(as_csv=True) should return a BinaryResponse."""
        result = await client.get_activity(as_csv=True)
        assert isinstance(result, BinaryResponse)
        assert result.content_type == "text/csv"


class TestZIPEndpoints:
    """Tests for ZIP-returning endpoints."""

    async def test_save_miner_stats(self, client: Any) -> None:
        """save_miner_stats should return a BinaryResponse with ZIP data."""
        result = await client.save_miner_stats()
        assert isinstance(result, BinaryResponse)
        assert "zip" in result.content_type
        assert result.data[:2] == b"PK"
        assert result.filename is not None
        assert result.filename.endswith(".zip")

    async def test_save_miner_stats_named(self, client: Any) -> None:
        """save_miner_stats with miner_name should not crash."""
        result = await client.save_miner_stats(miner_name="TRex")
        assert isinstance(result, BinaryResponse)

    async def test_get_debug_zip(self, client: Any) -> None:
        """get_debug_zip should return a BinaryResponse with ZIP data."""
        result = await client.get_debug_zip()
        assert isinstance(result, BinaryResponse)
        assert "zip" in result.content_type
        assert result.data[:2] == b"PK"
        assert result.filename is not None
        assert result.filename.endswith(".zip")
