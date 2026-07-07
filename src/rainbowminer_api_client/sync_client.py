"""Synchronous wrapper around :class:`RainbowMinerClient`.

This class provides a blocking interface for callers that are not running in
an async context.  It owns a private :mod:`asyncio` event loop and an
internal :class:`RainbowMinerClient` instance, so callers never need to
touch ``asyncio.run()``.

Example:
    ```python
    from rainbowminer_api_client import SyncRainbowMinerClient

    with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
        profit = client.get_current_profit()
        print(f"Current profit: {profit.ProfitBTC} BTC")
    ```

Parity with :class:`RainbowMinerClient` is enforced by
``tests/test_sync_client.py``.  When adding a new async method to
``RainbowMinerClient``, add the sync counterpart here in the same change.
"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from types import TracebackType
from typing import TYPE_CHECKING, Any

from rainbowminer_api_client._http import BinaryResponse
from rainbowminer_api_client.client import RainbowMinerClient
from rainbowminer_api_client.models.balances import Balance, EarningsResult, Payout
from rainbowminer_api_client.models.common import (
    ComputerStats,
    CPUInfo,
    Status,
    SysInfo,
    Uptime,
    Version,
)
from rainbowminer_api_client.models.config import (
    Config,
    LoadConfigJsonResult,
    SaveResult,
    SetupJson,
    UserConfig,
)
from rainbowminer_api_client.models.console import Console
from rainbowminer_api_client.models.devices import (
    AllDevice,
    Device,
    DeviceCombo,
    DeviceConfigEntry,
    OCProfile,
)
from rainbowminer_api_client.models.miners import (
    ActiveMiner,
    AsyncloaderJob,
    AvailMinerStat,
    FailedMiner,
    FastestMiner,
    Miner,
    MinerInfo,
    MinerLogResult,
    MinerSpeed,
    MinerStat,
    RemoteMiner,
    RemoteMinerEntry,
    RunningMiner,
)
from rainbowminer_api_client.models.misc import (
    Client,
    RateTableRow,
    ToggleResult,
)
from rainbowminer_api_client.models.mrr import MrrControl, MrrRig, MrrStat
from rainbowminer_api_client.models.pools import AllPool, NewPool, Pool
from rainbowminer_api_client.models.profit import CurrentProfit, DownloadItem, Total

if TYPE_CHECKING:
    pass

__all__ = ["SyncRainbowMinerClient"]

_DEFAULT_HOST = "localhost"
_DEFAULT_PORT = 4000
_DEFAULT_TIMEOUT = 30.0


class SyncRainbowMinerClient:
    """Blocking client for a RainbowMiner API server.

    Wraps :class:`RainbowMinerClient` with a private event loop so that
    every method can be called synchronously.  Use it as a context manager
    for automatic cleanup, or call :meth:`close` manually.
    """

    def __init__(
        self,
        host: str = _DEFAULT_HOST,
        port: int = _DEFAULT_PORT,
        *,
        username: str | None = None,
        password: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
        tls: bool = False,
    ) -> None:
        """Configure the sync client and its private event loop.

        Args:
            host: Hostname or IP address of the RainbowMiner server.
            port: TCP port the API server listens on (default ``4000``).
            username: Optional username for HTTP Basic auth.
            password: Optional password for HTTP Basic auth.
            timeout: Request timeout in seconds.
            tls: If ``True``, use ``https://`` instead of ``http://``.
        """
        self._loop = asyncio.new_event_loop()
        self._closed = False
        self._async_client: RainbowMinerClient = self._loop.run_until_complete(
            self._create_client(host, port, username, password, timeout, tls)
        )

    @staticmethod
    async def _create_client(
        host: str,
        port: int,
        username: str | None,
        password: str | None,
        timeout: float,
        tls: bool,
    ) -> RainbowMinerClient:
        """Create the internal async client within the event loop.

        Args:
            host: Hostname or IP address.
            port: TCP port.
            username: Optional auth username.
            password: Optional auth password.
            timeout: Request timeout in seconds.
            tls: Whether to use HTTPS.

        Returns:
            A configured :class:`RainbowMinerClient` instance.
        """
        return RainbowMinerClient(
            host=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            tls=tls,
        )

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #
    def close(self) -> None:
        """Close the underlying async client and the private event loop."""
        if self._closed:
            return
        self._closed = True
        try:
            self._loop.run_until_complete(self._async_client.close())
        finally:
            self._loop.close()

    def __enter__(self) -> SyncRainbowMinerClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def _run(self, coro: Any) -> Any:
        """Run a coroutine on the private event loop.

        Args:
            coro: The coroutine to run.

        Returns:
            The coroutine's result.
        """
        if self._closed:
            coro.close()  # Prevent "coroutine was never awaited" warning.
            raise RuntimeError("SyncRainbowMinerClient is closed")
        return self._loop.run_until_complete(coro)

    # ================================================================== #
    # Monitoring (read) endpoints — sync mirrors of RainbowMinerClient
    # ================================================================== #

    def get_version(self) -> Version:
        """Get the RainbowMiner version (``/version``)."""
        return self._run(self._async_client.get_version())

    def get_info(self) -> Any:
        """Get server info (``/info``)."""
        return self._run(self._async_client.get_info())

    def get_remote_ip(self) -> str | None:
        """Get the server's remote IP address (``/remoteip``)."""
        return self._run(self._async_client.get_remote_ip())

    def get_console(self, *, ts: int | None = None) -> Console:
        """Get the console output and running miner logs (``/console``)."""
        return self._run(self._async_client.get_console(ts=ts))

    def get_cpu_info(self) -> CPUInfo:
        """Get CPU information (``/cpuinfo``)."""
        return self._run(self._async_client.get_cpu_info())

    def get_sys_info(self) -> SysInfo:
        """Get system information (``/sysinfo``)."""
        return self._run(self._async_client.get_sys_info())

    def get_uptime(self) -> Uptime:
        """Get RainbowMiner uptime (``/uptime``)."""
        return self._run(self._async_client.get_uptime())

    def get_system_uptime(self) -> Uptime:
        """Get the operating system uptime (``/systemuptime``)."""
        return self._run(self._async_client.get_system_uptime())

    def is_server(self) -> bool:
        """Check whether the server runs in server mode (``/isserver``)."""
        return self._run(self._async_client.is_server())

    def get_active_miners(self) -> list[ActiveMiner]:
        """Get currently active miners (``/activeminers``)."""
        return self._run(self._async_client.get_active_miners())

    def get_running_miners(self) -> list[RunningMiner]:
        """Get currently running miners (``/runningminers``)."""
        return self._run(self._async_client.get_running_miners())

    def get_failed_miners(self) -> list[FailedMiner]:
        """Get miners that failed to start (``/failedminers``)."""
        return self._run(self._async_client.get_failed_miners())

    def get_remote_miners(self, *, mode: str | None = None) -> list[RemoteMiner] | list[RemoteMinerEntry]:
        """Get remote miners connected to a server (``/remoteminers``)."""
        return self._run(self._async_client.get_remote_miners(mode=mode))

    def get_miners_needing_benchmark(self) -> list[Any]:
        """Get miners that need benchmarking (``/minersneedingbenchmark``)."""
        return self._run(self._async_client.get_miners_needing_benchmark())

    def get_miner_info(self) -> list[MinerInfo]:
        """Get miner capability info (``/minerinfo``)."""
        return self._run(self._async_client.get_miner_info())

    def get_miner_speeds(self) -> list[MinerSpeed]:
        """Get miner hashrate speeds (``/minerspeeds``)."""
        return self._run(self._async_client.get_miner_speeds())

    def get_pools(self) -> list[Pool]:
        """Get active/enabled pools (``/pools``)."""
        return self._run(self._async_client.get_pools())

    def get_all_pools(self) -> list[AllPool]:
        """Get all known pools (``/allpools``)."""
        return self._run(self._async_client.get_all_pools())

    def get_new_pools(self) -> list[NewPool]:
        """Get newly discovered pools (``/newpools``)."""
        return self._run(self._async_client.get_new_pools())

    def get_algorithms(self) -> list[str]:
        """Get supported algorithms (``/algorithms``)."""
        return self._run(self._async_client.get_algorithms())

    def get_miners(self) -> list[Miner]:
        """Get available miner definitions (``/miners``)."""
        return self._run(self._async_client.get_miners())

    def get_fastest_miners(self) -> list[FastestMiner]:
        """Get the fastest miners per algorithm/device (``/fastestminers``)."""
        return self._run(self._async_client.get_fastest_miners())

    def get_avail_miners(self) -> list[str]:
        """Get the list of available miner base names (``/availminers``)."""
        return self._run(self._async_client.get_avail_miners())

    def get_avail_miner_stats(self) -> list[AvailMinerStat]:
        """Get available miners with stat counts (``/availminerstats``)."""
        return self._run(self._async_client.get_avail_miner_stats())

    def get_disabled(self) -> list[str]:
        """Get the list of disabled miners/pools (``/disabled``)."""
        return self._run(self._async_client.get_disabled())

    def get_wtm_urls(self) -> dict[str, str]:
        """Get WhatToMine URLs per device model (``/getwtmurls``)."""
        return self._run(self._async_client.get_wtm_urls())

    def load_config_json(self, *, config_name: str | None = None) -> LoadConfigJsonResult:
        """Load a raw config file as JSON string (``/loadconfigjson``)."""
        return self._run(self._async_client.load_config_json(config_name=config_name))

    def load_config(
        self,
        *,
        config_name: str | None = None,
        pool_name: str | None = None,
    ) -> Any:
        """Load a config section (``/loadconfig``)."""
        return self._run(self._async_client.load_config(config_name=config_name, pool_name=pool_name))

    def get_config(self) -> Config:
        """Get the merged running config (``/config``)."""
        return self._run(self._async_client.get_config())

    def get_user_config(self) -> UserConfig:
        """Get user config overrides (``/userconfig``)."""
        return self._run(self._async_client.get_user_config())

    def get_oc_profiles(self) -> list[OCProfile]:
        """Get overclock profiles (``/ocprofiles``)."""
        return self._run(self._async_client.get_oc_profiles())

    def get_download_list(self) -> list[DownloadItem]:
        """Get the download queue (``/downloadlist``)."""
        return self._run(self._async_client.get_download_list())

    def get_all_devices(self) -> list[AllDevice]:
        """Get all hardware devices (``/alldevices``)."""
        return self._run(self._async_client.get_all_devices())

    def get_devices(self) -> list[Device]:
        """Get selected/enabled devices (``/devices``)."""
        return self._run(self._async_client.get_devices())

    def get_platforms(self) -> dict[str, Any]:
        """Get OpenCL platform info (``/platforms``)."""
        return self._run(self._async_client.get_platforms())

    def get_device_combos(self) -> list[DeviceCombo]:
        """Get device combinations (``/devicecombos``)."""
        return self._run(self._async_client.get_device_combos())

    def get_device_config(self) -> list[DeviceConfigEntry]:
        """Get device selection/exclusion state (``/getdeviceconfig``)."""
        return self._run(self._async_client.get_device_config())

    def get_stats(self) -> dict[str, Any]:
        """Get the stats cache (``/stats``)."""
        return self._run(self._async_client.get_stats())

    def get_totals(self) -> list[Total]:
        """Get profit/power totals (``/totals``)."""
        return self._run(self._async_client.get_totals())

    def get_totals_csv(self) -> BinaryResponse:
        """Get totals as CSV (``/totalscsv``)."""
        return self._run(self._async_client.get_totals_csv())

    def get_earnings(
        self,
        *,
        filter: Mapping[str, Any] | None = None,
        sort: str = "Date",
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> EarningsResult:
        """Get earnings with optional filtering, sorting, and paging (``/earnings``)."""
        return self._run(
            self._async_client.get_earnings(filter=filter, sort=sort, order=order, limit=limit, offset=offset)
        )

    def get_earnings_csv(self) -> BinaryResponse:
        """Get earnings as CSV (``/earnings?as_csv=true``)."""
        return self._run(self._async_client.get_earnings_csv())

    def get_session_vars(self) -> dict[str, Any]:
        """Get scalar session variables (``/sessionvars``)."""
        return self._run(self._async_client.get_session_vars())

    def get_session(self) -> dict[str, Any]:
        """Get the full session hashtable (``/session``)."""
        return self._run(self._async_client.get_session())

    def get_gc(self) -> dict[str, Any]:
        """Get the sync-cache contents (``/gc``)."""
        return self._run(self._async_client.get_gc())

    def get_watchdog_timers(self) -> list[Any]:
        """Get watchdog timers (``/watchdogtimers``)."""
        return self._run(self._async_client.get_watchdog_timers())

    def get_crash_counter(self) -> list[Any]:
        """Get crash counter entries (``/crashcounter``)."""
        return self._run(self._async_client.get_crash_counter())

    def get_balances(
        self,
        *,
        raw: bool = False,
        add_total: bool = False,
        add_wallets: bool = False,
        add_btc: bool = False,
        consolidate: bool = False,
        as_csv: bool = False,
    ) -> list[Balance] | BinaryResponse:
        """Get balance information (``/balances``)."""
        return self._run(
            self._async_client.get_balances(
                raw=raw,
                add_total=add_total,
                add_wallets=add_wallets,
                add_btc=add_btc,
                consolidate=consolidate,
                as_csv=as_csv,
            )
        )

    def get_payouts(self) -> list[Payout]:
        """Get payout history (``/payouts``)."""
        return self._run(self._async_client.get_payouts())

    def get_rates(self, *, format: str | None = None) -> dict[str, float | int] | list[RateTableRow]:
        """Get currency exchange rates (``/rates``)."""
        return self._run(self._async_client.get_rates(format=format))

    def get_asyncloader_jobs(self) -> list[AsyncloaderJob]:
        """Get async loader jobs (``/asyncloaderjobs``)."""
        return self._run(self._async_client.get_asyncloader_jobs())

    def get_dec_sep(self) -> str:
        """Get the system's decimal separator (``/decsep``)."""
        return self._run(self._async_client.get_dec_sep())

    def get_miner_log(self, *, logfile: str | None = None) -> MinerLogResult:
        """Get the contents of a specific miner log file (``/getminerlog``)."""
        return self._run(self._async_client.get_miner_log(logfile=logfile))

    def get_miner_stats(self) -> list[MinerStat]:
        """Get benchmark stats for all miners (``/minerstats``)."""
        return self._run(self._async_client.get_miner_stats())

    def get_activity(self, *, as_csv: bool = False) -> list[Any] | BinaryResponse:
        """Get mining activity history (``/activity``)."""
        return self._run(self._async_client.get_activity(as_csv=as_csv))

    def get_computer_stats(self) -> ComputerStats:
        """Get computer statistics (``/computerstats``)."""
        return self._run(self._async_client.get_computer_stats())

    def get_miner_ports(self) -> dict[str, Any]:
        """Get miner port assignments (``/minerports``)."""
        return self._run(self._async_client.get_miner_ports())

    def get_current_profit(self) -> CurrentProfit:
        """Get current profit, earnings, rates, power, and uptime (``/currentprofit``)."""
        return self._run(self._async_client.get_current_profit())

    def get_status(self) -> Status:
        """Get the current mining status (``/status``)."""
        return self._run(self._async_client.get_status())

    def get_clients(self, *, include_server: bool = False) -> list[Client]:
        """Get connected RainbowMiner clients (``/clients``)."""
        return self._run(self._async_client.get_clients(include_server=include_server))

    def get_mrr_stats(self) -> list[MrrStat]:
        """Get MiningRigRentals algorithm stats (``/mrrstats``)."""
        return self._run(self._async_client.get_mrr_stats())

    def get_mrr_rigs(self) -> list[MrrRig]:
        """Get MiningRigRentals rig data (``/mrrrigs``)."""
        return self._run(self._async_client.get_mrr_rigs())

    def get_mrr_control(self) -> list[MrrControl]:
        """Get MiningRigRentals control settings (``/mrrcontrol``)."""
        return self._run(self._async_client.get_mrr_control())

    def get_setup(self) -> SetupJson:
        """Get the aggregated setup configuration (``/setup.json``)."""
        return self._run(self._async_client.get_setup())

    # ================================================================== #
    # Control (write) endpoints — sync mirrors of RainbowMinerClient
    # ================================================================== #

    def set_cmd_key(self, cmd_key: str) -> str:
        """Set the command menu key (``/cmdkey``)."""
        return self._run(self._async_client.set_cmd_key(cmd_key))

    def save_config_json(self, *, config_name: str | None = None, data: str) -> SaveResult:
        """Save a raw JSON config string (``/saveconfigjson``)."""
        return self._run(self._async_client.save_config_json(config_name=config_name, data=data))

    def save_config(self, *, config_name: str | None = None, **fields: Any) -> SaveResult:
        """Save config fields (``/saveconfig``)."""
        return self._run(self._async_client.save_config(config_name=config_name, **fields))

    def stop(self) -> str:
        """Stop the RainbowMiner server (``/stop``)."""
        return self._run(self._async_client.stop())

    def reboot(self) -> str:
        """Reboot the machine running RainbowMiner (``/reboot``)."""
        return self._run(self._async_client.reboot())

    def pause(self, *, action: str | None = None) -> bool:
        """Pause or unpause mining (``/pause``)."""
        return self._run(self._async_client.pause(action=action))

    def lock_miners(self) -> bool:
        """Toggle miner selection lock (``/lockminers``)."""
        return self._run(self._async_client.lock_miners())

    def reset_workers(self) -> str:
        """Reset offline workers on api.rbminer.net (``/resetworkers``)."""
        return self._run(self._async_client.reset_workers())

    def apply_oc(self) -> str:
        """Apply overclock profiles (``/applyoc``)."""
        return self._run(self._async_client.apply_oc())

    def update(self) -> bool:
        """Trigger a RainbowMiner self-update (``/update``)."""
        return self._run(self._async_client.update())

    def update_balance(self) -> bool:
        """Trigger a balance update (``/updatebalance``)."""
        return self._run(self._async_client.update_balance())

    def update_mrr(self) -> bool:
        """Trigger a MiningRigRentals update (``/updatemrr``)."""
        return self._run(self._async_client.update_mrr())

    def watchdog_reset(self) -> bool:
        """Reset watchdog timers (``/watchdogreset``)."""
        return self._run(self._async_client.watchdog_reset())

    def toggle_miner(self, *, name: str, algorithm: str, device_model: str) -> ToggleResult:
        """Enable or disable a miner (``/action/toggleminer``)."""
        return self._run(self._async_client.toggle_miner(name=name, algorithm=algorithm, device_model=device_model))

    def toggle_pool(
        self,
        *,
        name: str,
        algorithm: str | None = None,
        coin_symbol: str | None = None,
    ) -> ToggleResult:
        """Enable or disable a pool (``/action/togglepool``)."""
        return self._run(self._async_client.toggle_pool(name=name, algorithm=algorithm, coin_symbol=coin_symbol))

    def save_miner_stats(self, *, miner_name: str | None = None) -> BinaryResponse:
        """Download miner stats as a ZIP archive (``/saveminerstats``)."""
        return self._run(self._async_client.save_miner_stats(miner_name=miner_name))

    def get_debug_zip(self) -> BinaryResponse:
        """Download a debug log archive (``/debug``)."""
        return self._run(self._async_client.get_debug_zip())
