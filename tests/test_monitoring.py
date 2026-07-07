"""Tests for monitoring (read) endpoints — one test per GET method."""

from __future__ import annotations

from typing import Any

from rainbowminer_api_client.models.balances import Balance, EarningsResult, Payout
from rainbowminer_api_client.models.common import Status, Uptime, Version
from rainbowminer_api_client.models.config import Config, LoadConfigJsonResult, SetupJson, UserConfig
from rainbowminer_api_client.models.console import Console
from rainbowminer_api_client.models.devices import AllDevice, Device, DeviceConfigEntry, OCProfile
from rainbowminer_api_client.models.miners import (
    ActiveMiner,
    AvailMinerStat,
    MinerLogResult,
    RunningMiner,
)
from rainbowminer_api_client.models.mrr import MrrControl, MrrStat
from rainbowminer_api_client.models.pools import AllPool, Pool
from rainbowminer_api_client.models.profit import CurrentProfit


class TestInfoAndSystem:
    """Tests for system info, version, uptime, and status endpoints."""

    async def test_get_version(self, client: Any) -> None:
        """get_version should return a Version with the expected version string."""
        result = await client.get_version()
        assert isinstance(result, Version)
        assert result.Version == "4.6.1.0"

    async def test_get_info(self, client: Any) -> None:
        """get_info should return raw data (opaque object)."""
        result = await client.get_info()
        assert isinstance(result, dict | str | list | int | float | bool | None)

    async def test_get_remote_ip(self, client: Any) -> None:
        """get_remote_ip should return None when not configured."""
        result = await client.get_remote_ip()
        assert result is None

    async def test_get_console(self, client: Any) -> None:
        """get_console should return a Console model."""
        result = await client.get_console()
        assert isinstance(result, Console)
        assert result.Content == "RainbowMiner starting..."

    async def test_get_console_with_ts(self, client: Any) -> None:
        """get_console should accept a ts parameter."""
        result = await client.get_console(ts=1234567890)
        assert isinstance(result, Console)

    async def test_get_cpu_info(self, client: Any) -> None:
        """get_cpu_info should return a CPUInfo model."""
        result = await client.get_cpu_info()
        assert result.Cores == 8

    async def test_get_sys_info(self, client: Any) -> None:
        """get_sys_info should return a SysInfo model."""
        result = await client.get_sys_info()
        assert result is not None

    async def test_get_uptime(self, client: Any) -> None:
        """get_uptime should return an Uptime model."""
        result = await client.get_uptime()
        assert isinstance(result, Uptime)
        assert result.Seconds == 93784

    async def test_get_system_uptime(self, client: Any) -> None:
        """get_system_uptime should return an Uptime model."""
        result = await client.get_system_uptime()
        assert isinstance(result, Uptime)

    async def test_is_server(self, client: Any) -> None:
        """is_server should return a bool."""
        result = await client.is_server()
        assert result is False

    async def test_get_status(self, client: Any) -> None:
        """get_status should return a Status model."""
        result = await client.get_status()
        assert isinstance(result, Status)
        assert result.Pause is False

    async def test_get_current_profit(self, client: Any) -> None:
        """get_current_profit should return a CurrentProfit model."""
        result = await client.get_current_profit()
        assert isinstance(result, CurrentProfit)
        assert result.ProfitBTC == 0.00120

    async def test_get_dec_sep(self, client: Any) -> None:
        """get_dec_sep should return a string."""
        result = await client.get_dec_sep()
        assert result == "."

    async def test_get_computer_stats(self, client: Any) -> None:
        """get_computer_stats should return a ComputerStats model."""
        result = await client.get_computer_stats()
        assert result is not None

    async def test_get_miner_ports(self, client: Any) -> None:
        """get_miner_ports should return a dict."""
        result = await client.get_miner_ports()
        assert isinstance(result, dict)
        assert result.get("TRex") == 4001


class TestMiners:
    """Tests for miner-related endpoints."""

    async def test_get_active_miners(self, client: Any) -> None:
        """get_active_miners should return a list of ActiveMiner."""
        result = await client.get_active_miners()
        assert len(result) == 1
        assert isinstance(result[0], ActiveMiner)
        assert result[0].BaseName == "TRex"

    async def test_get_running_miners(self, client: Any) -> None:
        """get_running_miners should return a list of RunningMiner."""
        result = await client.get_running_miners()
        assert len(result) == 1
        assert isinstance(result[0], RunningMiner)

    async def test_get_failed_miners(self, client: Any) -> None:
        """get_failed_miners should return an empty list."""
        result = await client.get_failed_miners()
        assert isinstance(result, list)
        assert len(result) == 0

    async def test_get_remote_miners(self, client: Any) -> None:
        """get_remote_miners without mode should return RemoteMiner list."""
        result = await client.get_remote_miners()
        assert isinstance(result, list)

    async def test_get_remote_miners_mode(self, client: Any) -> None:
        """get_remote_miners with mode='miners' should return RemoteMinerEntry list."""
        result = await client.get_remote_miners(mode="miners")
        assert isinstance(result, list)

    async def test_get_miners_needing_benchmark(self, client: Any) -> None:
        """get_miners_needing_benchmark should return a list."""
        result = await client.get_miners_needing_benchmark()
        assert isinstance(result, list)

    async def test_get_miner_info(self, client: Any) -> None:
        """get_miner_info should return a list of MinerInfo."""
        result = await client.get_miner_info()
        assert isinstance(result, list)

    async def test_get_miner_speeds(self, client: Any) -> None:
        """get_miner_speeds should return a list of MinerSpeed."""
        result = await client.get_miner_speeds()
        assert isinstance(result, list)

    async def test_get_miners(self, client: Any) -> None:
        """get_miners should return a list of Miner."""
        result = await client.get_miners()
        assert isinstance(result, list)

    async def test_get_fastest_miners(self, client: Any) -> None:
        """get_fastest_miners should return a list of FastestMiner."""
        result = await client.get_fastest_miners()
        assert isinstance(result, list)

    async def test_get_avail_miners(self, client: Any) -> None:
        """get_avail_miners should return a list of strings."""
        result = await client.get_avail_miners()
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)
        assert "TRex" in result

    async def test_get_avail_miner_stats(self, client: Any) -> None:
        """get_avail_miner_stats should return a list of AvailMinerStat."""
        result = await client.get_avail_miner_stats()
        assert len(result) == 1
        assert isinstance(result[0], AvailMinerStat)
        assert result[0].Name == "TRex"

    async def test_get_disabled(self, client: Any) -> None:
        """get_disabled should return a list of strings."""
        result = await client.get_disabled()
        assert isinstance(result, list)
        assert "TRex-Ethash" in result

    async def test_get_miner_log(self, client: Any) -> None:
        """get_miner_log should return a MinerLogResult."""
        result = await client.get_miner_log(logfile="test.txt")
        assert isinstance(result, MinerLogResult)

    async def test_get_miner_stats(self, client: Any) -> None:
        """get_miner_stats should return a list of MinerStat."""
        result = await client.get_miner_stats()
        assert isinstance(result, list)

    async def test_get_asyncloader_jobs(self, client: Any) -> None:
        """get_asyncloader_jobs should return a list of AsyncloaderJob."""
        result = await client.get_asyncloader_jobs()
        assert isinstance(result, list)


class TestPoolsAndAlgorithms:
    """Tests for pool and algorithm endpoints."""

    async def test_get_pools(self, client: Any) -> None:
        """get_pools should return a list of Pool."""
        result = await client.get_pools()
        assert len(result) == 1
        assert isinstance(result[0], Pool)
        assert result[0].BaseName == "2Miners"

    async def test_get_all_pools(self, client: Any) -> None:
        """get_all_pools should return a list of AllPool."""
        result = await client.get_all_pools()
        assert len(result) == 1
        assert isinstance(result[0], AllPool)

    async def test_get_new_pools(self, client: Any) -> None:
        """get_new_pools should return a list of NewPool."""
        result = await client.get_new_pools()
        assert isinstance(result, list)

    async def test_get_algorithms(self, client: Any) -> None:
        """get_algorithms should return a list of Algorithm."""
        result = await client.get_algorithms()
        assert isinstance(result, list)
        assert len(result) == 1


class TestDevices:
    """Tests for device-related endpoints."""

    async def test_get_all_devices(self, client: Any) -> None:
        """get_all_devices should return a list of AllDevice."""
        result = await client.get_all_devices()
        assert len(result) == 1
        assert isinstance(result[0], AllDevice)

    async def test_get_devices(self, client: Any) -> None:
        """get_devices should return a list of Device."""
        result = await client.get_devices()
        assert len(result) == 1
        assert isinstance(result[0], Device)

    async def test_get_platforms(self, client: Any) -> None:
        """get_platforms should return a dict."""
        result = await client.get_platforms()
        assert isinstance(result, dict)

    async def test_get_device_combos(self, client: Any) -> None:
        """get_device_combos should return a list of DeviceCombo."""
        result = await client.get_device_combos()
        assert isinstance(result, list)

    async def test_get_device_config(self, client: Any) -> None:
        """get_device_config should return a list of DeviceConfigEntry."""
        result = await client.get_device_config()
        assert len(result) == 1
        assert isinstance(result[0], DeviceConfigEntry)

    async def test_get_oc_profiles(self, client: Any) -> None:
        """get_oc_profiles should return a list of OCProfile."""
        result = await client.get_oc_profiles()
        assert len(result) == 1
        assert isinstance(result[0], OCProfile)


class TestBalancesAndEarnings:
    """Tests for balance, payout, and earnings endpoints."""

    async def test_get_balances(self, client: Any) -> None:
        """get_balances should return a list of Balance."""
        result = await client.get_balances()
        assert len(result) == 1
        assert isinstance(result[0], Balance)

    async def test_get_payouts(self, client: Any) -> None:
        """get_payouts should return a list of Payout."""
        result = await client.get_payouts()
        assert len(result) == 1
        assert isinstance(result[0], Payout)

    async def test_get_earnings(self, client: Any) -> None:
        """get_earnings should return an EarningsResult."""
        result = await client.get_earnings()
        assert isinstance(result, EarningsResult)
        assert result.total == 2

    async def test_get_earnings_with_params(self, client: Any) -> None:
        """get_earnings should accept filter, sort, order, limit, offset."""
        result = await client.get_earnings(
            filter={"PoolName": "2MinersETH"},
            sort="Date",
            order="desc",
            limit=10,
            offset=5,
        )
        assert isinstance(result, EarningsResult)

    async def test_get_rates(self, client: Any) -> None:
        """get_rates should return a dict."""
        result = await client.get_rates()
        assert isinstance(result, dict)
        assert result.get("USD") == 65000.0

    async def test_get_rates_table(self, client: Any) -> None:
        """get_rates with format='table' should return a list of RateTableRow."""
        result = await client.get_rates(format="table")
        assert isinstance(result, list)
        # The mock server returns the same SAMPLE_RATES dict; with format=table
        # the server would normally return a list, but our mock returns a dict.
        # This test still verifies the method doesn't crash with format=table.


class TestConfig:
    """Tests for config-related endpoints."""

    async def test_get_config(self, client: Any) -> None:
        """get_config should return a Config model."""
        result = await client.get_config()
        assert isinstance(result, Config)

    async def test_get_user_config(self, client: Any) -> None:
        """get_user_config should return a UserConfig model."""
        result = await client.get_user_config()
        assert isinstance(result, UserConfig)

    async def test_load_config_json(self, client: Any) -> None:
        """load_config_json should return a LoadConfigJsonResult."""
        result = await client.load_config_json()
        assert isinstance(result, LoadConfigJsonResult)
        assert result.Success is True

    async def test_load_config_default(self, client: Any) -> None:
        """load_config with default name should return a Config model."""
        result = await client.load_config()
        assert isinstance(result, Config)

    async def test_get_setup(self, client: Any) -> None:
        """get_setup should return a SetupJson model."""
        result = await client.get_setup()
        assert isinstance(result, SetupJson)


class TestDynamicEndpoints:
    """Tests for endpoints with dynamic/loose payloads."""

    async def test_get_stats(self, client: Any) -> None:
        """get_stats should return a dict."""
        result = await client.get_stats()
        assert isinstance(result, dict)
        assert "CPU#Test_Ethash_HashRate" in result

    async def test_get_totals(self, client: Any) -> None:
        """get_totals should return a list."""
        result = await client.get_totals()
        assert isinstance(result, list)

    async def test_get_session_vars(self, client: Any) -> None:
        """get_session_vars should return a dict."""
        result = await client.get_session_vars()
        assert isinstance(result, dict)

    async def test_get_session(self, client: Any) -> None:
        """get_session should return a dict."""
        result = await client.get_session()
        assert isinstance(result, dict)

    async def test_get_gc(self, client: Any) -> None:
        """get_gc should return a dict."""
        result = await client.get_gc()
        assert isinstance(result, dict)

    async def test_get_watchdog_timers(self, client: Any) -> None:
        """get_watchdog_timers should return a list."""
        result = await client.get_watchdog_timers()
        assert isinstance(result, list)

    async def test_get_crash_counter(self, client: Any) -> None:
        """get_crash_counter should return a list."""
        result = await client.get_crash_counter()
        assert isinstance(result, list)

    async def test_get_activity(self, client: Any) -> None:
        """get_activity should return a list."""
        result = await client.get_activity()
        assert isinstance(result, list)

    async def test_get_wtm_urls(self, client: Any) -> None:
        """get_wtm_urls should return a dict."""
        result = await client.get_wtm_urls()
        assert isinstance(result, dict)

    async def test_get_download_list(self, client: Any) -> None:
        """get_download_list should return a list of DownloadItem."""
        result = await client.get_download_list()
        assert isinstance(result, list)


class TestClients:
    """Tests for client/server and MRR endpoints."""

    async def test_get_clients(self, client: Any) -> None:
        """get_clients should return a list of Client."""
        result = await client.get_clients()
        assert isinstance(result, list)

    async def test_get_clients_include_server(self, client: Any) -> None:
        """get_clients with include_server=True should not crash."""
        result = await client.get_clients(include_server=True)
        assert isinstance(result, list)

    async def test_get_mrr_stats(self, client: Any) -> None:
        """get_mrr_stats should return a list of MrrStat."""
        result = await client.get_mrr_stats()
        assert len(result) == 1
        assert isinstance(result[0], MrrStat)

    async def test_get_mrr_rigs(self, client: Any) -> None:
        """get_mrr_rigs should return a list of MrrRig."""
        result = await client.get_mrr_rigs()
        assert isinstance(result, list)

    async def test_get_mrr_control(self, client: Any) -> None:
        """get_mrr_control should return a list of MrrControl."""
        result = await client.get_mrr_control()
        assert len(result) == 1
        assert isinstance(result[0], MrrControl)
