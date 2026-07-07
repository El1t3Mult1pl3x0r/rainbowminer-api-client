"""Models for activity and watchdog endpoints.

Covers: ``/activity``, ``/watchdogtimers``, ``/crashcounter``.
"""

from __future__ import annotations

from typing import Any

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = ["Activity", "CrashCounter", "WatchdogTimer"]


class Activity(RainbowMinerModel):
    """An entry from ``/activity`` — a mining activity record.

    Attributes:
        ActiveStart: Activity start timestamp.
        ActiveLast: Last seen active timestamp.
        Name: Miner name.
        Device: Device identifiers.
        Algorithm: Algorithm(s) mined.
        Pool: Pool(s) used.
        Speed: Hashrate(s).
        Ratio: Efficiency ratio(s).
        Crashed: Whether the miner crashed.
        OCmode: Whether OC mode was active.
        OCP: OC profile applied.
        Profit: Average profit during the activity.
        PowerDraw: Average power draw in watts.
        TotalPowerDraw: Total energy consumed (Wh).
        TotalProfit: Total profit earned.
        Active: Duration in minutes.
        Donation: Whether this was a donation run.
    """

    ActiveStart: str | None = None
    ActiveLast: str | None = None
    Name: str | None = None
    Device: list[str] | None = None
    Algorithm: list[str] | None = None
    Pool: list[str] | None = None
    Speed: list[Any] | None = None
    Ratio: list[Any] | None = None
    Crashed: bool = False
    OCmode: bool = False
    OCP: dict[str, Any] | None = None
    Profit: float | int | None = None
    PowerDraw: float | int | None = None
    TotalPowerDraw: float | int | None = None
    TotalProfit: float | int | None = None
    Active: float | int | None = None
    Donation: bool = False


class WatchdogTimer(RainbowMinerModel):
    """An entry from ``/watchdogtimers``."""


class CrashCounter(RainbowMinerModel):
    """An entry from ``/crashcounter``."""
