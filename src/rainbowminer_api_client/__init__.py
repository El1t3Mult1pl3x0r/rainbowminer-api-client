"""rainbowminer-api-client — a typed Python client for the RainbowMiner API.

This package provides an async-first client
(:class:`RainbowMinerClient`) and a sync wrapper
(:class:`SyncRainbowMinerClient`) for communicating with a RainbowMiner
server's local HTTP API.  It is designed for integration into Home Assistant
or other Python applications that need to monitor or control a RainbowMiner
instance.

Quick start (async):
    ```python
    import asyncio
    from rainbowminer_api_client import RainbowMinerClient


    async def main() -> None:
        async with RainbowMinerClient("192.168.1.50", 4000) as client:
            profit = await client.get_current_profit()
            print(profit.ProfitBTC)


    asyncio.run(main())
    ```

Quick start (sync):
    ```python
    from rainbowminer_api_client import SyncRainbowMinerClient

    with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
        profit = client.get_current_profit()
        print(profit.ProfitBTC)
    ```
"""

from __future__ import annotations

from rainbowminer_api_client._http import BinaryResponse
from rainbowminer_api_client.client import RainbowMinerClient
from rainbowminer_api_client.errors import (
    RainbowMinerAPIError,
    RainbowMinerAuthError,
    RainbowMinerConnectionError,
    RainbowMinerError,
    RainbowMinerNotFoundError,
)
from rainbowminer_api_client.models import (
    ActiveMiner,
    Activity,
    Algorithm,
    AllDevice,
    AllPool,
    AsyncloaderJob,
    AvailMinerStat,
    Balance,
    Client,
    Config,
    Console,
    ConsoleMiner,
    CPUInfo,
    CrashCounter,
    CurrentProfit,
    Device,
    DeviceCombo,
    DeviceConfigEntry,
    DownloadItem,
    Earning,
    EarningsResult,
    FailedMiner,
    FastestMiner,
    IsServer,
    LoadConfigJsonResult,
    MinerConfig,
    MinerInfo,
    MinerLogResult,
    MinerPorts,
    MinerSpeed,
    MinerStat,
    MrrControl,
    MrrRig,
    MrrStat,
    NewPool,
    OCProfile,
    Payout,
    Pool,
    PoolsConfig,
    RainbowMinerModel,
    RatesDict,
    RateTableRow,
    RemoteMiner,
    RemoteMinerEntry,
    RunningMiner,
    SaveResult,
    SetupJson,
    StatsCache,
    Status,
    StringList,
    SysInfo,
    ToggleResult,
    Total,
    Uptime,
    UserConfig,
    Version,
    WatchdogTimer,
    WtmUrls,
)
from rainbowminer_api_client.sync_client import SyncRainbowMinerClient

__all__ = [
    "ActiveMiner",
    "Activity",
    "Algorithm",
    "AllDevice",
    "AllPool",
    "AsyncloaderJob",
    "AvailMinerStat",
    "Balance",
    # http
    "BinaryResponse",
    "CPUInfo",
    "Client",
    "ComputerStats",
    "Config",
    "Console",
    "ConsoleMiner",
    "CrashCounter",
    "CurrentProfit",
    "Device",
    "DeviceCombo",
    "DeviceConfigEntry",
    "DownloadItem",
    "Earning",
    "EarningsResult",
    "FailedMiner",
    "FastestMiner",
    "GarbageCollection",
    "IsServer",
    "LoadConfigJsonResult",
    "Miner",
    "MinerConfig",
    "MinerInfo",
    "MinerLogResult",
    "MinerPorts",
    "MinerSpeed",
    "MinerStat",
    "MrrControl",
    "MrrRig",
    "MrrStat",
    "NewPool",
    "OCProfile",
    "Payout",
    "Platforms",
    "Pool",
    "PoolsConfig",
    "RainbowMinerAPIError",
    "RainbowMinerAuthError",
    # clients
    "RainbowMinerClient",
    "RainbowMinerConnectionError",
    # errors
    "RainbowMinerError",
    # models
    "RainbowMinerModel",
    "RainbowMinerNotFoundError",
    "RateTableRow",
    "RatesDict",
    "RemoteMiner",
    "RemoteMinerEntry",
    "RunningMiner",
    "SaveResult",
    "Session",
    "SessionVars",
    "SetupJson",
    "StatsCache",
    "Status",
    "StringList",
    "SyncRainbowMinerClient",
    "SysInfo",
    "ToggleResult",
    "Total",
    "Uptime",
    "UserConfig",
    "Version",
    "WatchdogTimer",
    "WtmUrls",
]
