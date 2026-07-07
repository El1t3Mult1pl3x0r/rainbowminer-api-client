"""Models for miner-related endpoints.

Covers: ``/activeminers``, ``/runningminers``, ``/failedminers``,
``/remoteminers``, ``/minersneedingbenchmark``, ``/minerinfo``,
``/minerspeeds``, ``/miners``, ``/fastestminers``, ``/availminers``,
``/availminerstats``, ``/minerstats``, ``/getminerlog``, ``/minerports``,
``/asyncloaderjobs``.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, RootModel

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = [
    "ActiveMiner",
    "AsyncloaderJob",
    "AvailMinerStat",
    "FailedMiner",
    "FastestMiner",
    "Miner",
    "MinerInfo",
    "MinerLogResult",
    "MinerNeedingBenchmark",
    "MinerPorts",
    "MinerSpeed",
    "MinerStat",
    "RemoteMiner",
    "RemoteMinerEntry",
    "RunningMiner",
    "StringList",
]


class _MinerBase(RainbowMinerModel):
    """Common fields present in many miner objects."""

    Name: str | None = None
    BaseName: str | None = None
    DeviceModel: str | None = None
    DeviceName: list[str] | None = None
    BaseAlgorithm: list[str] | str | None = None
    Algorithm: list[str] | str | None = None
    SecondaryAlgorithm: str | None = None
    Pool: list[str] | str | None = None
    Speed: list[float | int] | float | int | None = None
    Ratio: list[float | int] | float | int | None = None
    PowerDraw: float | int | None = None
    Profit: float | int | None = None
    Path: str | None = None
    LogFile: str | None = None


class ActiveMiner(_MinerBase):
    """An entry from ``/activeminers``."""


class RunningMiner(_MinerBase):
    """An entry from ``/runningminers``."""


class FailedMiner(_MinerBase):
    """An entry from ``/failedminers``."""


class RemoteMiner(RainbowMinerModel):
    """An entry from ``/remoteminers`` (default mode).

    Attributes:
        online: Whether the remote miner is reachable.
        worker: Worker name of the remote miner.
        data: Miner data payload (dynamic).
    """

    online: bool = False
    worker: str | None = None
    data: list[Any] | dict[str, Any] | None = None


class RemoteMinerEntry(_MinerBase):
    """An entry from ``/remoteminers?mode=miners`` — flattened miner data.

    Attributes:
        Worker: The originating worker name.
    """

    Worker: str | None = None


class MinerNeedingBenchmark(RainbowMinerModel):
    """An entry from ``/minersneedingbenchmark``."""


class MinerInfo(RainbowMinerModel):
    """An entry from ``/minerinfo`` (miner capability info)."""


class MinerSpeed(RainbowMinerModel):
    """An entry from ``/minerspeeds``."""


class Miner(RainbowMinerModel):
    """An entry from ``/miners`` (available miner definitions).

    Attributes:
        BaseName: Miner binary base name.
        Path: Path to the miner executable.
    """

    BaseName: str | None = None
    Path: str | None = None


class FastestMiner(RainbowMinerModel):
    """An entry from ``/fastestminers``."""


class AvailMinerStat(RainbowMinerModel):
    """An entry from ``/availminerstats``.

    Attributes:
        Name: Miner base name.
        Statcount: Number of stored hashrate stats.
    """

    Name: str = ""
    Statcount: int = 0


class MinerStat(RainbowMinerModel):
    """An entry from ``/minerstats``.

    Attributes:
        BaseName: Miner binary base name.
        Name: Full miner name.
        Algorithm: Primary algorithm.
        SecondaryAlgorithm: Secondary algorithm (dual mining).
        Speed: Hashrate values.
        Ratio: Efficiency ratios.
        PowerDraw: Power consumption in watts.
        Devices: Device model label.
        DeviceModel: Raw device model identifier.
        Benchmarking: Whether the miner is currently benchmarking.
        NeedsBenchmark: Whether benchmark data is stale.
        BenchmarkFailed: Whether the last benchmark failed.
        Benchmarked: Timestamp of last successful benchmark.
        LogFile: Associated log file name.
    """

    BaseName: str | None = None
    Name: str | None = None
    Algorithm: str | None = None
    SecondaryAlgorithm: str = ""
    Speed: list[Any] = Field(default_factory=list)
    Ratio: list[Any] = Field(default_factory=list)
    PowerDraw: float | int | None = None
    Devices: str | None = None
    DeviceModel: str | None = None
    MSIAprofile: str | None = None
    OCprofile: str | None = None
    Benchmarking: bool = False
    NeedsBenchmark: bool = False
    BenchmarkFailed: bool = False
    Benchmarked: str | None = None
    LogFile: str = ""


class MinerLogResult(RainbowMinerModel):
    """Response of ``/getminerlog``.

    Attributes:
        Status: ``True`` if the log file was found.
        Content: The log file contents.
    """

    Status: bool = False
    Content: str = ""


class MinerPorts(RootModel[dict[str, Any]]):
    """Response of ``/minerports`` — mapping of miner names to port numbers."""


class AsyncloaderJob(RainbowMinerModel):
    """An entry from ``/asyncloaderjobs``."""


class StringList(RootModel[list[str]]):
    """A simple list-of-strings response (e.g. ``/availminers``, ``/disabled``)."""
