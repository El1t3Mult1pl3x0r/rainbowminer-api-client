"""Asynchronous client for the RainbowMiner local HTTP API.

The :class:`RainbowMinerClient` is the primary interface.  It is async-first
to integrate naturally with Home Assistant and other async Python
applications.  For non-async callers, use
:class:`~rainbowminer_api_client.sync_client.SyncRainbowMinerClient`.

Example:
    ```python
    import asyncio
    from rainbowminer_api_client import RainbowMinerClient


    async def main() -> None:
        async with RainbowMinerClient("192.168.1.50", 4000) as client:
            profit = await client.get_current_profit()
            print(f"Current profit: {profit.ProfitBTC} BTC")


    asyncio.run(main())
    ```
"""

from __future__ import annotations

from collections.abc import Mapping
from types import TracebackType
from typing import TYPE_CHECKING, Any

import aiohttp

from rainbowminer_api_client._http import BinaryResponse, HttpTransport
from rainbowminer_api_client.models.balances import Balance, EarningsResult, Payout
from rainbowminer_api_client.models.common import (
    ComputerStats,
    CPUInfo,
    GarbageCollection,
    IsServer,
    Platforms,
    Session,
    SessionVars,
    Status,
    SysInfo,
    Uptime,
    Version,
)
from rainbowminer_api_client.models.config import (
    Config,
    LoadConfigJsonResult,
    MinerConfig,
    PoolsConfig,
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
    MinerPorts,
    MinerSpeed,
    MinerStat,
    RemoteMiner,
    RemoteMinerEntry,
    RunningMiner,
    StringList,
)
from rainbowminer_api_client.models.misc import (
    Client,
    RatesDict,
    RateTableRow,
    ToggleResult,
    WtmUrls,
)
from rainbowminer_api_client.models.mrr import MrrControl, MrrRig, MrrStat
from rainbowminer_api_client.models.pools import AllPool, NewPool, Pool
from rainbowminer_api_client.models.profit import CurrentProfit, DownloadItem, StatsCache, Total

if TYPE_CHECKING:
    pass

__all__ = ["RainbowMinerClient"]

_DEFAULT_HOST = "localhost"
_DEFAULT_PORT = 4000
_DEFAULT_TIMEOUT = 30.0


class RainbowMinerClient:
    """Async client for a RainbowMiner API server.

    The client wraps an :class:`~rainbowminer_api_client._http.HttpTransport`
    and provides one typed method per API endpoint.  Use it as an async
    context manager for automatic session cleanup, or call :meth:`close`
    manually.
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
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Configure the client.

        Args:
            host: Hostname or IP address of the RainbowMiner server.
            port: TCP port the API server listens on (default ``4000``).
            username: Optional username for HTTP Basic auth.
            password: Optional password for HTTP Basic auth.
            timeout: Request timeout in seconds.
            tls: If ``True``, use ``https://`` instead of ``http://``.
            session: An existing :class:`aiohttp.ClientSession` to reuse.  If
                ``None``, a session will be created internally and closed by
                :meth:`close`.
        """
        self._transport = HttpTransport(
            host=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            tls=tls,
            session=session,
        )

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #
    async def close(self) -> None:
        """Close the underlying HTTP session if it was created internally."""
        await self._transport.close()

    async def __aenter__(self) -> RainbowMinerClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    # ================================================================== #
    # Monitoring (read) endpoints
    # ================================================================== #

    async def get_version(self) -> Version:
        """Get the RainbowMiner version (``/version``)."""
        return Version.model_validate(await self._transport.get_json("/version"))

    async def get_info(self) -> Any:
        """Get server info (``/info``).

        The ``/info`` payload is opaque and server-defined; it is returned as
        a raw Python object (typically a dict).
        """
        return await self._transport.get_json("/info")

    async def get_remote_ip(self) -> str | None:
        """Get the server's remote IP address (``/remoteip``).

        Returns:
            The remote IP string, or ``None`` if the server is not reachable
            remotely.
        """
        data = await self._transport.get_json("/remoteip")
        return data if isinstance(data, str) else None

    async def get_console(self, *, ts: int | None = None) -> Console:
        """Get the console output and running miner logs (``/console``).

        Args:
            ts: Last-seen console timestamp.  If it matches the server's
                current timestamp, the server returns ``"*"`` for the content
                (meaning "unchanged").

        Returns:
            A :class:`~rainbowminer_api_client.models.console.Console` object.
        """
        data = await self._transport.get_json("/console", params={"ts": ts} if ts is not None else None)
        return Console.model_validate(data)

    async def get_cpu_info(self) -> CPUInfo:
        """Get CPU information (``/cpuinfo``)."""
        return CPUInfo.model_validate(await self._transport.get_json("/cpuinfo"))

    async def get_sys_info(self) -> SysInfo:
        """Get system information (``/sysinfo``)."""
        return SysInfo.model_validate(await self._transport.get_json("/sysinfo"))

    async def get_uptime(self) -> Uptime:
        """Get RainbowMiner uptime (``/uptime``)."""
        return Uptime.model_validate(await self._transport.get_json("/uptime"))

    async def get_system_uptime(self) -> Uptime:
        """Get the operating system uptime (``/systemuptime``)."""
        return Uptime.model_validate(await self._transport.get_json("/systemuptime"))

    async def is_server(self) -> bool:
        """Check whether the server runs in server mode (``/isserver``)."""
        return IsServer.model_validate(await self._transport.get_json("/isserver")).Status

    async def get_active_miners(self) -> list[ActiveMiner]:
        """Get currently active miners (``/activeminers``)."""
        data = await self._transport.get_json("/activeminers")
        return [ActiveMiner.model_validate(item) for item in _as_list(data)]

    async def get_running_miners(self) -> list[RunningMiner]:
        """Get currently running miners (``/runningminers``)."""
        data = await self._transport.get_json("/runningminers")
        return [RunningMiner.model_validate(item) for item in _as_list(data)]

    async def get_failed_miners(self) -> list[FailedMiner]:
        """Get miners that failed to start (``/failedminers``)."""
        data = await self._transport.get_json("/failedminers")
        return [FailedMiner.model_validate(item) for item in _as_list(data)]

    async def get_remote_miners(self, *, mode: str | None = None) -> list[RemoteMiner] | list[RemoteMinerEntry]:
        """Get remote miners connected to a server (``/remoteminers``).

        Args:
            mode: If ``"miners"``, returns flattened per-miner entries
                (:class:`RemoteMinerEntry`).  Otherwise returns per-worker
                summaries (:class:`RemoteMiner`).

        Returns:
            A list of miner objects whose type depends on ``mode``.
        """
        params: dict[str, str | None] = {"Mode": mode}
        data = await self._transport.get_json("/remoteminers", params=params)
        items = _as_list(data)
        if mode == "miners":
            return [RemoteMinerEntry.model_validate(item) for item in items]
        return [RemoteMiner.model_validate(item) for item in items]

    async def get_miners_needing_benchmark(self) -> list[Any]:
        """Get miners that need benchmarking (``/minersneedingbenchmark``)."""
        data = await self._transport.get_json("/minersneedingbenchmark")
        return _as_list(data)

    async def get_miner_info(self) -> list[MinerInfo]:
        """Get miner capability info (``/minerinfo``)."""
        data = await self._transport.get_json("/minerinfo")
        return [MinerInfo.model_validate(item) for item in _as_list(data)]

    async def get_miner_speeds(self) -> list[MinerSpeed]:
        """Get miner hashrate speeds (``/minerspeeds``)."""
        data = await self._transport.get_json("/minerspeeds")
        return [MinerSpeed.model_validate(item) for item in _as_list(data)]

    async def get_pools(self) -> list[Pool]:
        """Get active/enabled pools (``/pools``)."""
        data = await self._transport.get_json("/pools")
        return [Pool.model_validate(item) for item in _as_list(data)]

    async def get_all_pools(self) -> list[AllPool]:
        """Get all known pools (``/allpools``)."""
        data = await self._transport.get_json("/allpools")
        return [AllPool.model_validate(item) for item in _as_list(data)]

    async def get_new_pools(self) -> list[NewPool]:
        """Get newly discovered pools (``/newpools``)."""
        data = await self._transport.get_json("/newpools")
        return [NewPool.model_validate(item) for item in _as_list(data)]

    async def get_algorithms(self) -> list[str]:
        """Get supported algorithms (``/algorithms``).

        The API returns a list of algorithm name strings (e.g.
        ``["Ethash", "Kawpow"]``).
        """
        data = await self._transport.get_json("/algorithms")
        return [str(item) for item in _as_list(data)]

    async def get_miners(self) -> list[Miner]:
        """Get available miner definitions (``/miners``)."""
        data = await self._transport.get_json("/miners")
        return [Miner.model_validate(item) for item in _as_list(data)]

    async def get_fastest_miners(self) -> list[FastestMiner]:
        """Get the fastest miners per algorithm/device (``/fastestminers``)."""
        data = await self._transport.get_json("/fastestminers")
        return [FastestMiner.model_validate(item) for item in _as_list(data)]

    async def get_avail_miners(self) -> list[str]:
        """Get the list of available miner base names (``/availminers``)."""
        data = await self._transport.get_json("/availminers")
        return StringList.model_validate(_as_list(data)).root

    async def get_avail_miner_stats(self) -> list[AvailMinerStat]:
        """Get available miners with stat counts (``/availminerstats``)."""
        data = await self._transport.get_json("/availminerstats")
        return [AvailMinerStat.model_validate(item) for item in _as_list(data)]

    async def get_disabled(self) -> list[str]:
        """Get the list of disabled miners/pools (``/disabled``)."""
        data = await self._transport.get_json("/disabled")
        return StringList.model_validate(_as_list(data)).root

    async def get_wtm_urls(self) -> dict[str, str]:
        """Get WhatToMine URLs per device model (``/getwtmurls``)."""
        data = await self._transport.get_json("/getwtmurls")
        return WtmUrls.model_validate(data).root

    async def load_config_json(self, *, config_name: str | None = None) -> LoadConfigJsonResult:
        """Load a raw config file as JSON string (``/loadconfigjson``).

        Args:
            config_name: Config file name (default ``"Config"``).

        Returns:
            A :class:`~rainbowminer_api_client.models.config.LoadConfigJsonResult`.
        """
        data = await self._transport.get_json("/loadconfigjson", params={"ConfigName": config_name})
        return LoadConfigJsonResult.model_validate(data)

    async def load_config(
        self,
        *,
        config_name: str | None = None,
        pool_name: str | None = None,
    ) -> Any:
        """Load a config section (``/loadconfig``).

        The return type varies by ``config_name``: ``"Config"`` returns a
        :class:`Config`, ``"Miners"`` returns ``list[MinerConfig]``,
        ``"Pools"`` returns a :class:`PoolsConfig`, and others return a raw
        object.  The result is therefore typed as ``Any``.

        Args:
            config_name: Config section name (default ``"Config"``).
            pool_name: Pool name filter (only for ``config_name="Pools"``).

        Returns:
            The loaded config section (type depends on ``config_name``).
        """
        params: dict[str, str | None] = {"ConfigName": config_name, "PoolName": pool_name}
        data = await self._transport.get_json("/loadconfig", params=params)
        if config_name == "Miners" and isinstance(data, list):
            return [MinerConfig.model_validate(item) for item in data]
        if config_name == "Pools":
            return PoolsConfig.model_validate(data)
        if config_name in (None, "Config"):
            return Config.model_validate(data)
        return data

    async def get_config(self) -> Config:
        """Get the merged running config (``/config``)."""
        return Config.model_validate(await self._transport.get_json("/config"))

    async def get_user_config(self) -> UserConfig:
        """Get user config overrides (``/userconfig``)."""
        return UserConfig.model_validate(await self._transport.get_json("/userconfig"))

    async def get_oc_profiles(self) -> list[OCProfile]:
        """Get overclock profiles (``/ocprofiles``)."""
        data = await self._transport.get_json("/ocprofiles")
        return [OCProfile.model_validate(item) for item in _as_list(data)]

    async def get_download_list(self) -> list[DownloadItem]:
        """Get the download queue (``/downloadlist``)."""
        data = await self._transport.get_json("/downloadlist")
        return [DownloadItem.model_validate(item) for item in _as_list(data)]

    async def get_all_devices(self) -> list[AllDevice]:
        """Get all hardware devices (``/alldevices``)."""
        data = await self._transport.get_json("/alldevices")
        return [AllDevice.model_validate(item) for item in _as_list(data)]

    async def get_devices(self) -> list[Device]:
        """Get selected/enabled devices (``/devices``)."""
        data = await self._transport.get_json("/devices")
        return [Device.model_validate(item) for item in _as_list(data)]

    async def get_platforms(self) -> dict[str, Any]:
        """Get OpenCL platform info (``/platforms``)."""
        data = await self._transport.get_json("/platforms")
        if data is None:
            return {}
        return Platforms.model_validate(data).root

    async def get_device_combos(self) -> list[DeviceCombo]:
        """Get device combinations (``/devicecombos``)."""
        data = await self._transport.get_json("/devicecombos")
        return [DeviceCombo.model_validate(item) for item in _as_list(data)]

    async def get_device_config(self) -> list[DeviceConfigEntry]:
        """Get device selection/exclusion state (``/getdeviceconfig``)."""
        data = await self._transport.get_json("/getdeviceconfig")
        return [DeviceConfigEntry.model_validate(item) for item in _as_list(data)]

    async def get_stats(self) -> dict[str, Any]:
        """Get the stats cache (``/stats``).

        The stats cache is highly dynamic; it is returned as a plain dict.
        """
        data = await self._transport.get_json("/stats")
        if data is None:
            return {}
        return StatsCache.model_validate(data).root

    async def get_totals(self) -> list[Total]:
        """Get profit/power totals (``/totals``)."""
        data = await self._transport.get_json("/totals")
        return [Total.model_validate(item) for item in _as_list(data)]

    async def get_totals_csv(self) -> BinaryResponse:
        """Get totals as CSV (``/totalscsv``).

        Returns:
            A :class:`~rainbowminer_api_client._http.BinaryResponse` with
            ``content_type="text/csv"``.
        """
        return await self._transport.get_binary("/totalscsv")

    async def get_earnings(
        self,
        *,
        filter: Mapping[str, Any] | None = None,
        sort: str = "Date",
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> EarningsResult:
        """Get earnings with optional filtering, sorting, and paging (``/earnings``).

        Args:
            filter: A mapping of field-name → value to filter by.
            sort: Sort field name (default ``"Date"``).
            order: ``"desc"`` for descending, otherwise ascending.
            limit: Maximum number of rows to return.
            offset: Number of rows to skip (used with ``limit``).

        Returns:
            An :class:`~rainbowminer_api_client.models.balances.EarningsResult`.
        """
        import json

        params: dict[str, str | int | None] = {
            "sort": sort,
            "order": order,
            "limit": limit,
            "offset": offset,
            "filter": json.dumps(filter) if filter else None,
        }
        data = await self._transport.get_json("/earnings", params=params)
        if data is None:
            return EarningsResult()
        return EarningsResult.model_validate(data)

    async def get_earnings_csv(self) -> BinaryResponse:
        """Get earnings as CSV (``/earnings?as_csv=true``).

        Returns:
            A :class:`~rainbowminer_api_client._http.BinaryResponse` with
            ``content_type="text/csv"``.
        """
        return await self._transport.get_binary("/earnings", params={"as_csv": "true"})

    async def get_session_vars(self) -> dict[str, Any]:
        """Get scalar session variables (``/sessionvars``)."""
        data = await self._transport.get_json("/sessionvars")
        if data is None:
            return {}
        return SessionVars.model_validate(data).root

    async def get_session(self) -> dict[str, Any]:
        """Get the full session hashtable (``/session``)."""
        data = await self._transport.get_json("/session")
        if data is None:
            return {}
        return Session.model_validate(data).root

    async def get_gc(self) -> dict[str, Any]:
        """Get the sync-cache contents (``/gc``)."""
        data = await self._transport.get_json("/gc")
        if data is None:
            return {}
        return GarbageCollection.model_validate(data).root

    async def get_watchdog_timers(self) -> list[Any]:
        """Get watchdog timers (``/watchdogtimers``)."""
        data = await self._transport.get_json("/watchdogtimers")
        return _as_list(data)

    async def get_crash_counter(self) -> list[Any]:
        """Get crash counter entries (``/crashcounter``)."""
        data = await self._transport.get_json("/crashcounter")
        return _as_list(data)

    async def get_balances(
        self,
        *,
        raw: bool = False,
        add_total: bool = False,
        add_wallets: bool = False,
        add_btc: bool = False,
        consolidate: bool = False,
        as_csv: bool = False,
    ) -> list[Balance] | BinaryResponse:
        """Get balance information (``/balances``).

        Args:
            raw: Return raw balances without filtering.
            add_total: Include total pool balance entries.
            add_wallets: Include wallet balance entries.
            add_btc: Add BTC-converted fields to each entry.
            consolidate: Consolidate balances by name (converted to BTC).
            as_csv: Return the balances as CSV instead of JSON.

        Returns:
            A list of :class:`~rainbowminer_api_client.models.balances.Balance`
            objects, or a :class:`~rainbowminer_api_client._http.BinaryResponse`
            if ``as_csv=True``.
        """
        params: dict[str, str | bool | None] = {
            "raw": raw if raw else None,
            "add_total": "true" if add_total else None,
            "add_wallets": "true" if add_wallets else None,
            "add_btc": "true" if add_btc else None,
            "consolidate": "true" if consolidate else None,
            "as_csv": "true" if as_csv else None,
        }
        if as_csv:
            return await self._transport.get_binary("/balances", params=params)
        data = await self._transport.get_json("/balances", params=params)
        return [Balance.model_validate(item) for item in _as_list(data)]

    async def get_payouts(self) -> list[Payout]:
        """Get payout history (``/payouts``)."""
        data = await self._transport.get_json("/payouts")
        return [Payout.model_validate(item) for item in _as_list(data)]

    async def get_rates(self, *, format: str | None = None) -> dict[str, float | int] | list[RateTableRow]:
        """Get currency exchange rates (``/rates``).

        Args:
            format: If ``"table"``, returns a list of
                :class:`~rainbowminer_api_client.models.misc.RateTableRow`
                objects.  Otherwise returns a currency → rate dict.

        Returns:
            Either a dict or a list of rate table rows, depending on ``format``.
        """
        params: dict[str, str | None] = {"format": format}
        data = await self._transport.get_json("/rates", params=params)
        if format == "table":
            return [RateTableRow.model_validate(item) for item in _as_list(data)]
        if data is None:
            return {}
        return RatesDict.model_validate(data).root

    async def get_asyncloader_jobs(self) -> list[AsyncloaderJob]:
        """Get async loader jobs (``/asyncloaderjobs``)."""
        data = await self._transport.get_json("/asyncloaderjobs")
        return [AsyncloaderJob.model_validate(item) for item in _as_list(data)]

    async def get_dec_sep(self) -> str:
        """Get the system's decimal separator (``/decsep``)."""
        data = await self._transport.get_json("/decsep")
        return data if isinstance(data, str) else str(data)

    async def get_miner_log(self, *, logfile: str | None = None) -> MinerLogResult:
        """Get the contents of a specific miner log file (``/getminerlog``).

        Args:
            logfile: The log file name to retrieve.

        Returns:
            A :class:`~rainbowminer_api_client.models.miners.MinerLogResult`.
        """
        data = await self._transport.get_json("/getminerlog", params={"logfile": logfile})
        return MinerLogResult.model_validate(data)

    async def get_miner_stats(self) -> list[MinerStat]:
        """Get benchmark stats for all miners (``/minerstats``)."""
        data = await self._transport.get_json("/minerstats")
        return [MinerStat.model_validate(item) for item in _as_list(data)]

    async def get_activity(self, *, as_csv: bool = False) -> list[Any] | BinaryResponse:
        """Get mining activity history (``/activity``).

        Args:
            as_csv: Return the activity as CSV instead of JSON.

        Returns:
            A list of activity objects (raw dicts, since the CSV and JSON
            shapes differ), or a
            :class:`~rainbowminer_api_client._http.BinaryResponse` if
            ``as_csv=True``.
        """
        params: dict[str, str | None] = {"as_csv": "true" if as_csv else None}
        if as_csv:
            return await self._transport.get_binary("/activity", params=params)
        data = await self._transport.get_json("/activity", params=params)
        return _as_list(data)

    async def get_computer_stats(self) -> ComputerStats:
        """Get computer statistics (``/computerstats``).

        The server returns ``null`` (HTTP 404) when computer stats are not yet
        available; in that case an empty :class:`ComputerStats` is returned.
        """
        data = await self._transport.get_json("/computerstats")
        return ComputerStats.model_validate(data if data is not None else {})

    async def get_miner_ports(self) -> dict[str, Any]:
        """Get miner port assignments (``/minerports``)."""
        data = await self._transport.get_json("/minerports")
        if data is None:
            return {}
        return MinerPorts.model_validate(data).root

    async def get_current_profit(self) -> CurrentProfit:
        """Get current profit, earnings, rates, power, and uptime (``/currentprofit``)."""
        return CurrentProfit.model_validate(await self._transport.get_json("/currentprofit"))

    async def get_status(self) -> Status:
        """Get the current mining status (``/status``)."""
        return Status.model_validate(await self._transport.get_json("/status"))

    async def get_clients(self, *, include_server: bool = False) -> list[Client]:
        """Get connected RainbowMiner clients (``/clients``).

        Args:
            include_server: Include the server itself in the list (only valid
                when the server runs in server mode).

        Returns:
            A list of :class:`~rainbowminer_api_client.models.misc.Client`.
        """
        params: dict[str, str | None] = {"include_server": "true" if include_server else None}
        data = await self._transport.get_json("/clients", params=params)
        return [Client.model_validate(item) for item in _as_list(data)]

    async def get_mrr_stats(self) -> list[MrrStat]:
        """Get MiningRigRentals algorithm stats (``/mrrstats``)."""
        data = await self._transport.get_json("/mrrstats")
        return [MrrStat.model_validate(item) for item in _as_list(data)]

    async def get_mrr_rigs(self) -> list[MrrRig]:
        """Get MiningRigRentals rig data (``/mrrrigs``)."""
        data = await self._transport.get_json("/mrrrigs")
        return [MrrRig.model_validate(item) for item in _as_list(data)]

    async def get_mrr_control(self) -> list[MrrControl]:
        """Get MiningRigRentals control settings (``/mrrcontrol``)."""
        data = await self._transport.get_json("/mrrcontrol")
        return [MrrControl.model_validate(item) for item in _as_list(data)]

    async def get_setup(self) -> SetupJson:
        """Get the aggregated setup configuration (``/setup.json``)."""
        return SetupJson.model_validate(await self._transport.get_json("/setup.json"))

    # ================================================================== #
    # Control (write) endpoints
    # ================================================================== #

    async def set_cmd_key(self, cmd_key: str) -> str:
        """Set the command menu key (``/cmdkey``).

        Args:
            cmd_key: The command key to set.

        Returns:
            The new command key value.
        """
        data = await self._transport.get_json("/cmdkey", params={"CmdKey": cmd_key})
        return data if isinstance(data, str) else str(data)

    async def save_config_json(self, *, config_name: str | None = None, data: str) -> SaveResult:
        """Save a raw JSON config string (``/saveconfigjson``).

        Args:
            config_name: Config file name (default ``"Config"``).
            data: The JSON config content as a string.

        Returns:
            A :class:`~rainbowminer_api_client.models.config.SaveResult`.
        """
        result = await self._transport.post_json(
            "/saveconfigjson",
            params={"ConfigName": config_name},
            data={"Data": data},
        )
        return SaveResult.model_validate(result)

    async def save_config(self, *, config_name: str | None = None, **fields: Any) -> SaveResult:
        """Save config fields (``/saveconfig``).

        Extra keyword arguments are sent as form fields to the server.

        Args:
            config_name: Config section name (default ``"Config"``).
            **fields: Config field name → value pairs to save.

        Returns:
            A :class:`~rainbowminer_api_client.models.config.SaveResult`.
        """
        params: dict[str, str | None] = {"ConfigName": config_name}
        form: dict[str, str] = {}
        for key, value in fields.items():
            if value is None:
                continue
            if isinstance(value, bool):
                form[key] = "1" if value else "0"
            elif isinstance(value, list):
                form[key] = ",".join(str(v) for v in value)
            else:
                form[key] = str(value)
        result = await self._transport.post_json("/saveconfig", params=params, data=form)
        return SaveResult.model_validate(result)

    async def stop(self) -> str:
        """Stop the RainbowMiner server (``/stop``)."""
        data = await self._transport.get_json("/stop")
        return data if isinstance(data, str) else str(data)

    async def reboot(self) -> str:
        """Reboot the machine running RainbowMiner (``/reboot``)."""
        data = await self._transport.get_json("/reboot")
        return data if isinstance(data, str) else str(data)

    async def pause(self, *, action: str | None = None) -> bool:
        """Pause or unpause mining (``/pause``).

        Args:
            action: One of ``"set"``, ``"reset"``, ``"pause"``, ``"unpause"``.
                If ``None``, the server pauses unconditionally.

        Returns:
            The new pause state (``True`` = paused).
        """
        params: dict[str, str | None] = {"action": action}
        data = await self._transport.get_json("/pause", params=params)
        return bool(data)

    async def lock_miners(self) -> bool:
        """Toggle miner selection lock (``/lockminers``).

        Returns:
            The new lock state (``True`` = locked).
        """
        return bool(await self._transport.get_json("/lockminers"))

    async def reset_workers(self) -> str:
        """Reset offline workers on api.rbminer.net (``/resetworkers``)."""
        data = await self._transport.get_json("/resetworkers")
        return data if isinstance(data, str) else str(data)

    async def apply_oc(self) -> str:
        """Apply overclock profiles (``/applyoc``)."""
        data = await self._transport.get_json("/applyoc")
        return data if isinstance(data, str) else str(data)

    async def update(self) -> bool:
        """Trigger a RainbowMiner self-update (``/update``)."""
        return bool(await self._transport.get_json("/update"))

    async def update_balance(self) -> bool:
        """Trigger a balance update (``/updatebalance``)."""
        return bool(await self._transport.get_json("/updatebalance"))

    async def update_mrr(self) -> bool:
        """Trigger a MiningRigRentals update (``/updatemrr``)."""
        return bool(await self._transport.get_json("/updatemrr"))

    async def watchdog_reset(self) -> bool:
        """Reset watchdog timers (``/watchdogreset``)."""
        return bool(await self._transport.get_json("/watchdogreset"))

    async def toggle_miner(self, *, name: str, algorithm: str, device_model: str) -> ToggleResult:
        """Enable or disable a miner (``/action/toggleminer``).

        Toggling a disabled miner re-enables it, and vice versa.

        Args:
            name: Miner base name.
            algorithm: Algorithm(s) the miner runs (dual-algo miners use
                ``-`` as separator).
            device_model: The device model identifier.

        Returns:
            A :class:`~rainbowminer_api_client.models.misc.ToggleResult`.
        """
        params: dict[str, str | None] = {
            "name": name,
            "algorithm": algorithm,
            "devicemodel": device_model,
        }
        data = await self._transport.get_json("/action/toggleminer", params=params)
        return ToggleResult.model_validate(data)

    async def toggle_pool(
        self,
        *,
        name: str,
        algorithm: str | None = None,
        coin_symbol: str | None = None,
    ) -> ToggleResult:
        """Enable or disable a pool (``/action/togglepool``).

        Either ``algorithm`` or ``coin_symbol`` must be provided.

        Args:
            name: Pool name.
            algorithm: Algorithm identifier (alternative to ``coin_symbol``).
            coin_symbol: Coin symbol (alternative to ``algorithm``).

        Returns:
            A :class:`~rainbowminer_api_client.models.misc.ToggleResult`.
        """
        params: dict[str, str | None] = {
            "name": name,
            "algorithm": algorithm,
            "coinsymbol": coin_symbol,
        }
        data = await self._transport.get_json("/action/togglepool", params=params)
        return ToggleResult.model_validate(data)

    async def save_miner_stats(self, *, miner_name: str | None = None) -> BinaryResponse:
        """Download miner stats as a ZIP archive (``/saveminerstats``).

        Args:
            miner_name: Miner base name, or ``None``/``"all"`` for all miners.

        Returns:
            A :class:`~rainbowminer_api_client._http.BinaryResponse` with
            ``content_type="application/zip"``.
        """
        return await self._transport.get_binary(
            "/saveminerstats",
            params={"MinerName": miner_name},
        )

    async def get_debug_zip(self) -> BinaryResponse:
        """Download a debug log archive (``/debug``).

        The ZIP contains recent log files with sensitive data (wallets, API
        keys, IPs) redacted.

        Returns:
            A :class:`~rainbowminer_api_client._http.BinaryResponse` with
            ``content_type="application/zip"``.
        """
        return await self._transport.get_binary("/debug")


def _as_list(data: Any) -> list[Any]:
    """Coerce an API response into a list.

    The RainbowMiner server returns ``"[]"`` (which parses to an empty list)
    or ``None`` for many endpoints when there is no data.  This helper
    normalises those cases to an empty list.

    Args:
        data: The raw parsed JSON response.

    Returns:
        A list of items, possibly empty.
    """
    if data is None:
        return []
    if isinstance(data, list):
        return data
    return [data]
