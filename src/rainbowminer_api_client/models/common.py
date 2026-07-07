"""Models for small, shared response objects.

Covers: ``/version``, ``/info``, ``/uptime``, ``/systemuptime``, ``/isserver``,
``/remoteip``, ``/status``, ``/decsep``, ``/sysinfo``, ``/cpuinfo``,
``/sessionvars``, ``/session``, ``/gc``, ``/platforms``.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, RootModel

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = [
    "CPUInfo",
    "ComputerStats",
    "GarbageCollection",
    "IsServer",
    "LockMinersState",
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

    The server returns a nested object with ``Version`` and ``RemoteVersion``
    fields, each a ``System.Version``-style object (Major, Minor, Build,
    Revision, ...).  For convenience the string form can be accessed via
    :meth:`version_string`.

    Attributes:
        Version: Local version as a version-object dict (or a plain string
            on older server versions).
        RemoteVersion: Remote/latest version object, or ``None``.
        Build: Optional build identifier (kept for backward compatibility).
    """

    Version: str | dict[str, Any] | None = None
    RemoteVersion: dict[str, Any] | None = None
    Build: str | None = None

    def version_string(self) -> str:
        """Return the version as a dotted string (e.g. ``"5.0.1.9"``).

        Handles both the object form (``{"Major": 5, "Minor": 0, ...}``)
        and the legacy plain-string form.
        """
        v = self.Version
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            parts = []
            for key in ("Major", "Minor", "Build", "Revision"):
                if key in v and v[key] is not None:
                    parts.append(str(v[key]))
            return ".".join(parts) if parts else ""
        return ""


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


class LockMinersState(RainbowMinerModel):
    """The nested ``LockMiners`` object inside :class:`Status`.

    Attributes:
        Enabled: Whether the lock feature is enabled.
        Locked: Whether miners are currently locked.
        Pools: List of locked pool names.
    """

    Enabled: bool = False
    Locked: bool = False
    Pools: list[str] = Field(default_factory=list)


class Status(RainbowMinerModel):
    """Response of ``/status``.

    Attributes:
        Pause: Whether miners are globally paused.
        PauseIAOnly: Whether only IA (idle-aware) miners are paused.
        LockMiners: Lock state — either a bool (legacy) or a
            :class:`LockMinersState` object (current servers).
        IsExclusiveRun: Whether the current run is exclusive.
        IsDonationRun: Whether the current run is a donation run.
    """

    Pause: bool = False
    PauseIAOnly: bool = False
    LockMiners: bool | LockMinersState = False
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
