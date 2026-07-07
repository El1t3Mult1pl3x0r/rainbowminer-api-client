"""Models package — Pydantic response models for the RainbowMiner API.

All response models derive from :class:`~rainbowminer_api_client.models._base.RainbowMinerModel`
which allows extra fields for forward-compatibility with future RainbowMiner
versions.
"""

from __future__ import annotations

from rainbowminer_api_client._http import BinaryResponse
from rainbowminer_api_client.models._base import RainbowMinerModel
from rainbowminer_api_client.models.activity import Activity, CrashCounter, WatchdogTimer
from rainbowminer_api_client.models.balances import Balance, Earning, EarningsResult, Payout
from rainbowminer_api_client.models.common import (
    ComputerStats,
    CPUInfo,
    GarbageCollection,
    IsServer,
    LockMinersState,
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
from rainbowminer_api_client.models.console import Console, ConsoleMiner
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
from rainbowminer_api_client.models.pools import Algorithm, AllPool, NewPool, Pool
from rainbowminer_api_client.models.profit import CurrentProfit, DownloadItem, StatsCache, Total

__all__ = [
    # miners
    "ActiveMiner",
    # activity / watchdog
    "Activity",
    "Algorithm",
    # devices
    "AllDevice",
    "AllPool",
    "AsyncloaderJob",
    "AvailMinerStat",
    # balances
    "Balance",
    "BinaryResponse",
    "CPUInfo",
    # misc
    "Client",
    "ComputerStats",
    # config
    "Config",
    # console
    "Console",
    "ConsoleMiner",
    "CrashCounter",
    # profit / stats
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
    "LockMinersState",
    "Miner",
    "MinerConfig",
    "MinerInfo",
    "MinerLogResult",
    "MinerPorts",
    "MinerSpeed",
    "MinerStat",
    "MrrControl",
    "MrrRig",
    # mrr
    "MrrStat",
    "NewPool",
    "OCProfile",
    "Payout",
    "Platforms",
    # pools
    "Pool",
    "PoolsConfig",
    # base
    "RainbowMinerModel",
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
    "SysInfo",
    "ToggleResult",
    "Total",
    "Uptime",
    "UserConfig",
    # common
    "Version",
    "WatchdogTimer",
    "WtmUrls",
]
