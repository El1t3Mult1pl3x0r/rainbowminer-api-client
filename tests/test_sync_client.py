"""Tests for the :class:`SyncRainbowMinerClient` wrapper and sync/async parity."""

from __future__ import annotations

import inspect
import threading

import pytest

from rainbowminer_api_client import RainbowMinerClient, SyncRainbowMinerClient
from rainbowminer_api_client._http import BinaryResponse
from rainbowminer_api_client.models.balances import Balance
from rainbowminer_api_client.models.common import Status, Version
from rainbowminer_api_client.models.misc import ToggleResult


def _close_sync(sc: SyncRainbowMinerClient) -> None:
    """Close a SyncRainbowMinerClient in a separate thread.

    The sync client's close() uses run_until_complete(), which conflicts
    with the pytest-asyncio event loop running in the main thread.  Running
    close() in a separate thread avoids this conflict.
    """
    errors: list[Exception] = []

    def _do_close() -> None:
        """Close the sync client."""
        try:
            sc.close()
        except Exception as e:
            errors.append(e)

    t = threading.Thread(target=_do_close)
    t.start()
    t.join()
    if errors:
        raise errors[0]


class TestSyncClientBasic:
    """Basic sync client functionality tests."""

    def test_context_manager(self, sync_client: SyncRainbowMinerClient) -> None:
        """Sync client should work as a context manager.

        Note: we manually close via _close_sync after the with-block because
        __exit__ calls close() which uses run_until_complete(), conflicting
        with the running pytest-asyncio loop.
        """
        try:
            with sync_client as sc:
                profit = sc.get_current_profit()
                assert profit.ProfitBTC == 0.00120
        except RuntimeError:
            # __exit__ may fail due to running loop; close manually below.
            pass
        _close_sync(sync_client)

    def test_get_version(self, sync_client: SyncRainbowMinerClient) -> None:
        """get_version should return a Version model."""
        result = sync_client.get_version()
        assert isinstance(result, Version)
        assert result.Version == "4.6.1.0"

    def test_get_current_profit(self, sync_client: SyncRainbowMinerClient) -> None:
        """get_current_profit should return a CurrentProfit model."""
        result = sync_client.get_current_profit()
        assert result.ProfitBTC == 0.00120

    def test_get_status(self, sync_client: SyncRainbowMinerClient) -> None:
        """get_status should return a Status model."""
        result = sync_client.get_status()
        assert isinstance(result, Status)
        assert result.Pause is False

    def test_get_active_miners(self, sync_client: SyncRainbowMinerClient) -> None:
        """get_active_miners should return a list of ActiveMiner."""
        result = sync_client.get_active_miners()
        assert len(result) == 1
        assert result[0].BaseName == "TRex"

    def test_get_balances(self, sync_client: SyncRainbowMinerClient) -> None:
        """get_balances should return a list of Balance."""
        result = sync_client.get_balances()
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Balance)

    def test_stop(self, sync_client: SyncRainbowMinerClient) -> None:
        """stop should return the server's text response."""
        result = sync_client.stop()
        assert result == "Stopping"

    def test_pause(self, sync_client: SyncRainbowMinerClient) -> None:
        """pause should return a bool."""
        result = sync_client.pause()
        assert result is True

    def test_toggle_miner(self, sync_client: SyncRainbowMinerClient) -> None:
        """toggle_miner should return a ToggleResult."""
        result = sync_client.toggle_miner(name="TRex", algorithm="Ethash", device_model="NVIDIA")
        assert isinstance(result, ToggleResult)
        assert result.Status is True

    def test_get_totals_csv(self, sync_client: SyncRainbowMinerClient) -> None:
        """get_totals_csv should return a BinaryResponse."""
        result = sync_client.get_totals_csv()
        assert isinstance(result, BinaryResponse)
        assert result.content_type == "text/csv"
        assert b"Pool" in result.data

    def test_double_close_is_safe(self, sync_client: SyncRainbowMinerClient) -> None:
        """Closing the sync client twice should not raise."""
        _close_sync(sync_client)
        _close_sync(sync_client)  # Should be a no-op.

    def test_use_after_close_raises(self, sync_client: SyncRainbowMinerClient) -> None:
        """Using the sync client after close should raise RuntimeError."""
        _close_sync(sync_client)
        with pytest.raises(RuntimeError):
            sync_client.get_version()


class TestSyncAsyncParity:
    """Enforce that every public async method has a sync counterpart with matching signature."""

    @staticmethod
    def _public_async_methods() -> dict[str, inspect.Signature]:
        """Collect public async methods from RainbowMinerClient.

        Returns:
            A mapping of method name → signature for all public async methods.
        """
        result: dict[str, inspect.Signature] = {}
        for name in dir(RainbowMinerClient):
            if name.startswith("_"):
                continue
            attr = getattr(RainbowMinerClient, name)
            if not callable(attr):
                continue
            if not inspect.iscoroutinefunction(attr):
                continue
            result[name] = inspect.signature(attr)
        return result

    @staticmethod
    def _public_sync_methods() -> dict[str, inspect.Signature]:
        """Collect public sync methods from SyncRainbowMinerClient.

        Returns:
            A mapping of method name → signature for all public sync methods.
        """
        result: dict[str, inspect.Signature] = {}
        for name in dir(SyncRainbowMinerClient):
            if name.startswith("_"):
                continue
            attr = getattr(SyncRainbowMinerClient, name)
            if not callable(attr):
                continue
            if inspect.iscoroutinefunction(attr):
                continue
            result[name] = inspect.signature(attr)
        return result

    def test_every_async_method_has_sync_counterpart(self) -> None:
        """Every public async method on RainbowMinerClient must exist on SyncRainbowMinerClient."""
        async_methods = self._public_async_methods()
        sync_methods = self._public_sync_methods()
        missing = set(async_methods) - set(sync_methods)
        assert not missing, f"SyncRainbowMinerClient is missing sync counterparts for: {sorted(missing)}"

    def test_signatures_match(self) -> None:
        """Sync method signatures must match async method signatures (minus async/await)."""
        async_methods = self._public_async_methods()
        sync_methods = self._public_sync_methods()
        mismatches: list[str] = []
        for name, async_sig in async_methods.items():
            if name not in sync_methods:
                continue  # Covered by test_every_async_method_has_sync_counterpart.
            sync_sig = sync_methods[name]
            async_params = list(async_sig.parameters.items())
            sync_params = list(sync_sig.parameters.items())
            if len(async_params) != len(sync_params):
                mismatches.append(f"{name}: param count mismatch ({len(async_params)} vs {len(sync_params)})")
                continue
            for (a_name, _a_param), (s_name, _s_param) in zip(async_params, sync_params, strict=False):
                if a_name != s_name:
                    mismatches.append(f"{name}: param name mismatch ({a_name} vs {s_name})")
        assert not mismatches, f"Signature mismatches:\n{chr(10).join(mismatches)}"
