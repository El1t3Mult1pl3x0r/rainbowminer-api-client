"""Registry of read-only (GET) endpoints for record-and-replay fixture testing.

Each entry maps a RainbowMiner API path to the Pydantic model that should
parse it, plus a ``kind`` describing how the raw JSON maps to the model:

- ``SINGLE``       — one model object (``Model.model_validate(data)``)
- ``LIST``         — a list of model objects (``[Model.model_validate(x) for x in data]``)
- ``STRING_LIST``  — a list of strings
- ``DICT``         — a ``dict[str, Any]`` wrapped by a root model
- ``RAW``          — opaque payload; only assert it is JSON-decodable

This registry is shared between :mod:`tests.record_fixtures` (record mode)
and :mod:`tests.test_replay_fixtures` (replay mode) so the two stay in sync.

Only endpoints that do **not** mutate server state are listed here.  Write /
control endpoints (``stop``, ``pause``, ``toggle_*``, ``save_*``, ``update*``,
``reboot``, ``applyoc``, ``resetworkers``, ``watchdogreset``, ``lockminers``,
``cmdkey``) are intentionally excluded.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from collections.abc import Mapping


class ParseKind(Enum):
    """How a raw JSON response maps to a Pydantic model."""

    SINGLE = "single"
    LIST = "list"
    STRING_LIST = "string_list"
    DICT = "dict"
    RAW = "raw"


@dataclass(frozen=True, slots=True)
class EndpointSpec:
    """Description of one read-only API endpoint.

    Attributes:
        path: The API path (must start with ``/``).
        name: The fixture file stem (without extension).
        kind: How to parse the response.
        model: The Pydantic model class (``None`` for ``RAW``/``STRING_LIST``).
        params: Optional query params to send when recording.
    """

    path: str
    name: str
    kind: ParseKind
    model: type[BaseModel] | None = None
    params: Mapping[str, str] | None = None


# Model imports kept here so the registry is the single source of truth.
from rainbowminer_api_client.models.balances import Balance, EarningsResult, Payout  # noqa: E402
from rainbowminer_api_client.models.common import (  # noqa: E402
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
from rainbowminer_api_client.models.config import (  # noqa: E402
    Config,
    LoadConfigJsonResult,
    SetupJson,
    UserConfig,
)
from rainbowminer_api_client.models.console import Console  # noqa: E402
from rainbowminer_api_client.models.devices import (  # noqa: E402
    AllDevice,
    Device,
    DeviceConfigEntry,
    OCProfile,
)
from rainbowminer_api_client.models.miners import (  # noqa: E402
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
)
from rainbowminer_api_client.models.misc import (  # noqa: E402
    Client,
    RatesDict,
    WtmUrls,
)
from rainbowminer_api_client.models.mrr import MrrControl, MrrRig, MrrStat  # noqa: E402
from rainbowminer_api_client.models.pools import AllPool, NewPool, Pool  # noqa: E402
from rainbowminer_api_client.models.profit import CurrentProfit, DownloadItem, StatsCache, Total  # noqa: E402

# --------------------------------------------------------------------------- #
# Read-only endpoint registry
# --------------------------------------------------------------------------- #
# fmt: off
READ_ONLY_ENDPOINTS: tuple[EndpointSpec, ...] = (
    # --- system / info (single object) ---
    EndpointSpec("/version",          "version",          ParseKind.SINGLE, Version),
    EndpointSpec("/console",          "console",          ParseKind.SINGLE, Console),
    EndpointSpec("/cpuinfo",           "cpuinfo",          ParseKind.SINGLE, CPUInfo),
    EndpointSpec("/sysinfo",           "sysinfo",          ParseKind.SINGLE, SysInfo),
    EndpointSpec("/uptime",            "uptime",           ParseKind.SINGLE, Uptime),
    EndpointSpec("/systemuptime",      "systemuptime",     ParseKind.SINGLE, Uptime),
    EndpointSpec("/isserver",          "isserver",         ParseKind.SINGLE, IsServer),
    EndpointSpec("/computerstats",    "computerstats",    ParseKind.SINGLE, ComputerStats),
    EndpointSpec("/currentprofit",     "currentprofit",    ParseKind.SINGLE, CurrentProfit),
    EndpointSpec("/status",            "status",           ParseKind.SINGLE, Status),
    EndpointSpec("/setup.json",        "setup",            ParseKind.SINGLE, SetupJson),
    EndpointSpec("/config",            "config",           ParseKind.SINGLE, Config),
    EndpointSpec("/userconfig",        "userconfig",       ParseKind.SINGLE, UserConfig),
    EndpointSpec("/loadconfigjson",    "loadconfigjson",   ParseKind.SINGLE, LoadConfigJsonResult),
    EndpointSpec("/getminerlog",       "getminerlog",      ParseKind.SINGLE, MinerLogResult),

    # --- list-of-model endpoints ---
    EndpointSpec("/activeminers",      "activeminers",     ParseKind.LIST, ActiveMiner),
    EndpointSpec("/runningminers",     "runningminers",    ParseKind.LIST, RunningMiner),
    EndpointSpec("/failedminers",      "failedminers",     ParseKind.LIST, FailedMiner),
    EndpointSpec("/remoteminers",      "remoteminers",     ParseKind.LIST, RemoteMiner),
    EndpointSpec(
        "/remoteminers", "remoteminers_mode", ParseKind.LIST, RemoteMinerEntry, params={"mode": "miners"}
    ),
    EndpointSpec("/minerinfo",          "minerinfo",        ParseKind.LIST, MinerInfo),
    EndpointSpec("/minerspeeds",       "minerspeeds",      ParseKind.LIST, MinerSpeed),
    EndpointSpec("/minerstats",        "minerstats",       ParseKind.LIST, MinerStat),
    EndpointSpec("/miners",            "miners",           ParseKind.LIST, Miner),
    EndpointSpec("/fastestminers",     "fastestminers",    ParseKind.LIST, FastestMiner),
    EndpointSpec("/availminerstats",   "availminerstats",  ParseKind.LIST, AvailMinerStat),
    EndpointSpec("/pools",             "pools",            ParseKind.LIST, Pool),
    EndpointSpec("/allpools",          "allpools",         ParseKind.LIST, AllPool),
    EndpointSpec("/newpools",          "newpools",         ParseKind.LIST, NewPool),
    EndpointSpec("/ocprofiles",        "ocprofiles",       ParseKind.LIST, OCProfile),
    EndpointSpec("/downloadlist",      "downloadlist",     ParseKind.LIST, DownloadItem),
    EndpointSpec("/alldevices",        "alldevices",       ParseKind.LIST, AllDevice),
    EndpointSpec("/devices",           "devices",          ParseKind.LIST, Device),
    EndpointSpec("/devicecombos",      "devicecombos",     ParseKind.STRING_LIST),
    EndpointSpec("/getdeviceconfig",   "getdeviceconfig",  ParseKind.LIST, DeviceConfigEntry),
    EndpointSpec("/totals",            "totals",           ParseKind.LIST, Total),
    EndpointSpec("/payouts",           "payouts",          ParseKind.LIST, Payout),
    EndpointSpec("/balances",          "balances",         ParseKind.LIST, Balance),
    EndpointSpec("/earnings",          "earnings",         ParseKind.SINGLE, EarningsResult),
    EndpointSpec("/asyncloaderjobs",   "asyncloaderjobs",  ParseKind.LIST, AsyncloaderJob),
    EndpointSpec("/clients",           "clients",          ParseKind.LIST, Client),
    EndpointSpec("/mrrstats",          "mrrstats",         ParseKind.LIST, MrrStat),
    EndpointSpec("/mrrrigs",           "mrrrigs",          ParseKind.LIST, MrrRig),
    EndpointSpec("/mrrcontrol",        "mrrcontrol",       ParseKind.LIST, MrrControl),

    # --- string-list endpoints ---
    EndpointSpec("/algorithms",       "algorithms",       ParseKind.STRING_LIST),
    EndpointSpec("/availminers",       "availminers",      ParseKind.STRING_LIST),
    EndpointSpec("/disabled",         "disabled",         ParseKind.STRING_LIST),

    # --- dict-wrapped endpoints ---
    EndpointSpec("/getwtmurls",        "getwtmurls",       ParseKind.DICT, WtmUrls),
    EndpointSpec("/platforms",         "platforms",        ParseKind.DICT, Platforms),
    EndpointSpec("/stats",             "stats",            ParseKind.DICT, StatsCache),
    EndpointSpec("/sessionvars",       "sessionvars",      ParseKind.DICT, SessionVars),
    EndpointSpec("/session",           "session",          ParseKind.DICT, Session),
    EndpointSpec("/gc",                "gc",               ParseKind.DICT, GarbageCollection),
    EndpointSpec("/minerports",        "minerports",       ParseKind.DICT, MinerPorts),
    EndpointSpec("/rates",             "rates",            ParseKind.DICT, RatesDict),

    # --- opaque / raw endpoints (no model; only assert JSON-decodable) ---
    EndpointSpec("/info",              "info",             ParseKind.RAW),
    EndpointSpec("/minersneedingbenchmark", "minersneedingbenchmark", ParseKind.RAW),
    EndpointSpec("/watchdogtimers",    "watchdogtimers",   ParseKind.RAW),
    EndpointSpec("/crashcounter",      "crashcounter",     ParseKind.RAW),
    EndpointSpec("/activity",          "activity",         ParseKind.RAW),
)
# fmt: on
