"""Tests for control (write) endpoints — verify correct paths and params."""

from __future__ import annotations

from typing import Any

import pytest

from rainbowminer_api_client.models.config import SaveResult
from rainbowminer_api_client.models.misc import ToggleResult


class TestStopReboot:
    """Tests for stop and reboot endpoints."""

    async def test_stop(self, client: Any) -> None:
        """stop should return the server's text response."""
        result = await client.stop()
        assert result == "Stopping"

    async def test_reboot(self, client: Any) -> None:
        """reboot should return a string message."""
        result = await client.reboot()
        assert isinstance(result, str)

    async def test_apply_oc(self, client: Any) -> None:
        """apply_oc should return a string message."""
        result = await client.apply_oc()
        assert isinstance(result, str)

    async def test_reset_workers(self, client: Any) -> None:
        """reset_workers should return a string message."""
        result = await client.reset_workers()
        assert isinstance(result, str)


class TestPauseAndLock:
    """Tests for pause and lock endpoints."""

    async def test_pause_default(self, client: Any) -> None:
        """pause without action should return a bool."""
        result = await client.pause()
        assert result is True

    async def test_pause_with_action(self, client: Any) -> None:
        """pause with action='unpause' should return a bool."""
        result = await client.pause(action="unpause")
        assert isinstance(result, bool)

    async def test_lock_miners(self, client: Any) -> None:
        """lock_miners should return a bool."""
        result = await client.lock_miners()
        assert isinstance(result, bool)


class TestUpdates:
    """Tests for update trigger endpoints."""

    async def test_update(self, client: Any) -> None:
        """update should return a bool."""
        result = await client.update()
        assert result is True

    async def test_update_balance(self, client: Any) -> None:
        """update_balance should return a bool."""
        result = await client.update_balance()
        assert isinstance(result, bool)

    async def test_update_mrr(self, client: Any) -> None:
        """update_mrr should return a bool."""
        result = await client.update_mrr()
        assert isinstance(result, bool)

    async def test_watchdog_reset(self, client: Any) -> None:
        """watchdog_reset should return a bool."""
        result = await client.watchdog_reset()
        assert isinstance(result, bool)


class TestToggleActions:
    """Tests for toggle miner/pool endpoints."""

    async def test_toggle_miner(self, client: Any) -> None:
        """toggle_miner should return a ToggleResult with Status and Disabled."""
        result = await client.toggle_miner(name="TRex", algorithm="Ethash", device_model="NVIDIA")
        assert isinstance(result, ToggleResult)
        assert result.Status is True
        assert result.Disabled is True

    async def test_toggle_miner_missing_params_raises(self, client: Any) -> None:
        """toggle_miner should raise TypeError when required params are missing."""
        with pytest.raises(TypeError):
            await client.toggle_miner(name="TRex")  # type: ignore[call-arg]  # algorithm and device_model are required

    async def test_toggle_pool_with_algorithm(self, client: Any) -> None:
        """toggle_pool with algorithm should return a ToggleResult."""
        result = await client.toggle_pool(name="2MinersETH", algorithm="Ethash")
        assert isinstance(result, ToggleResult)

    async def test_toggle_pool_with_coin_symbol(self, client: Any) -> None:
        """toggle_pool with coin_symbol should return a ToggleResult."""
        result = await client.toggle_pool(name="2MinersETH", coin_symbol="ETH")
        assert isinstance(result, ToggleResult)


class TestConfigWrites:
    """Tests for config write endpoints."""

    async def test_set_cmd_key(self, client: Any) -> None:
        """set_cmd_key should return the key string."""
        result = await client.set_cmd_key("a")
        assert result == "a"

    async def test_save_config_json(self, client: Any) -> None:
        """save_config_json should return a SaveResult."""
        result = await client.save_config_json(data='{"WorkerName":"test"}')
        assert isinstance(result, SaveResult)
        assert result.Success is True

    async def test_save_config(self, client: Any) -> None:
        """save_config should return a SaveResult."""
        result = await client.save_config(config_name="Config", WorkerName="test")
        assert isinstance(result, SaveResult)
        assert result.Success is True

    async def test_save_config_with_list_value(self, client: Any) -> None:
        """save_config should handle list values by joining with commas."""
        result = await client.save_config(config_name="Config", PoolName=["2Miners", "Nanopool"])
        assert isinstance(result, SaveResult)

    async def test_save_config_with_bool_value(self, client: Any) -> None:
        """save_config should convert bool values to '1'/'0'."""
        result = await client.save_config(config_name="Config", EnableRestartComputer=True)
        assert isinstance(result, SaveResult)

    async def test_save_config_skips_none(self, client: Any) -> None:
        """save_config should skip None values."""
        result = await client.save_config(config_name="Config", WorkerName=None, PoolName="2Miners")
        assert isinstance(result, SaveResult)


class TestWriteParamVerification:
    """Verify that control methods send the correct query params to the server."""

    @pytest.mark.usefixtures("aiohttp_client")
    async def test_pause_sends_action_param(self, aiohttp_client: Any) -> None:
        """pause(action='unpause') should send action=unpause query param."""
        from aiohttp import web

        captured: dict[str, str] = {}

        async def pause_handler(request: web.Request) -> web.Response:
            """Capture the action query param."""
            captured.update(dict(request.query))
            return web.json_response(True)

        app = web.Application()
        app.router.add_get("/pause", pause_handler)
        test_client = await aiohttp_client(app)

        from rainbowminer_api_client import RainbowMinerClient

        client = RainbowMinerClient(host="127.0.0.1", port=test_client.port)
        client._transport._session = test_client.session
        client._transport._owns_session = False

        await client.pause(action="unpause")
        assert captured.get("action") == "unpause"

    @pytest.mark.usefixtures("aiohttp_client")
    async def test_toggle_miner_sends_params(self, aiohttp_client: Any) -> None:
        """toggle_miner should send name, algorithm, devicemodel params."""
        from aiohttp import web

        captured: dict[str, str] = {}

        async def toggle_handler(request: web.Request) -> web.Response:
            """Capture the toggle miner query params."""
            captured.update(dict(request.query))
            return web.json_response({"Status": True, "Disabled": True})

        app = web.Application()
        app.router.add_get("/action/toggleminer", toggle_handler)
        test_client = await aiohttp_client(app)

        from rainbowminer_api_client import RainbowMinerClient

        client = RainbowMinerClient(host="127.0.0.1", port=test_client.port)
        client._transport._session = test_client.session
        client._transport._owns_session = False

        await client.toggle_miner(name="TRex", algorithm="Ethash", device_model="NVIDIA")
        assert captured.get("name") == "TRex"
        assert captured.get("algorithm") == "Ethash"
        assert captured.get("devicemodel") == "NVIDIA"
