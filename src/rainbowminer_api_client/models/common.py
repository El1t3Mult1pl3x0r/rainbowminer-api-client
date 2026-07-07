"""Models for small, shared response objects.

Covers: ``/version``, ``/info``, ``/uptime``, ``/systemuptime``, ``/isserver``,
``/remoteip``, ``/status``, ``/decsep``, ``/sysinfo``, ``/cpuinfo``,
``/sessionvars``, ``/session``, ``/gc``, ``/platforms``.
"""

from __future__ import annotations

from typing import Any

from pydantic import RootModel

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = [
    "CPUInfo",
    "ComputerStats",
    "GarbageCollection",
    "IsServer",
    "Platforms",
    "Session",
    "SessionVars",
    "Status",
    "SysInfo",
    "Uptime",
    "Version",
]


class Version(RainbowMinerModel):
    """Version of the RainbowMiner server (``/version``).

    Attributes:
        Version: Version string (e.g. ``"5.4.1.2"``).
        Build: Optional build identifier.
    """

    Version: str | None = None
    Build: str | None = None


class Uptime(RainbowMinerModel):
    """Uptime duration returned by ``/uptime`` and ``/systemuptime``.

    Attributes:
        AsString: Human-readable duration like ``"1.02:03:04"``.
        Seconds: Total uptime in seconds.
    """

    AsString: str = ""
    Seconds: int = 0


class IsServer(RainbowMinerModel):
    """Response of ``/isserver``.

    Attributes:
        Status: ``True`` if the server runs in server mode.
    """

    Status: bool = False


class Status(RainbowMinerModel):
    """Response of ``/status``.

    Attributes:
        Pause: Whether miners are globally paused.
        PauseIAOnly: Whether only IA (idle-aware) miners are paused.
        LockMiners: Whether miner selection is locked.
        IsExclusiveRun: Whether the current run is exclusive.
        IsDonationRun: Whether the current run is a donation run.
    """

    Pause: bool = False
    PauseIAOnly: bool = False
    LockMiners: bool = False
    IsExclusiveRun: bool = False
    IsDonationRun: bool = False


class ComputerStats(RainbowMinerModel):
    """Response of ``/computerstats`` (opaque, server-defined fields)."""


class SysInfo(RainbowMinerModel):
    """Response of ``/sysinfo`` (system hardware info, server-defined)."""


class CPUInfo(RainbowMinerModel):
    """Response of ``/cpuinfo`` (CPU info, server-defined)."""


class SessionVars(RootModel[dict[str, Any]]):
    """Response of ``/sessionvars`` — a flat mapping of scalar session vars."""


class Session(RootModel[dict[str, Any]]):
    """Response of ``/session`` — the full session hashtable (dynamic)."""


class GarbageCollection(RootModel[dict[str, Any]]):
    """Response of ``/gc`` — the sync-cache contents (dynamic)."""


class Platforms(RootModel[dict[str, Any]]):
    """Response of ``/platforms`` — OpenCL platform info (dynamic).

    Parsed from a JSON file; structure varies by system.
    """
