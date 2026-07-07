"""Models for profit, totals, and stats endpoints.

Covers: ``/currentprofit``, ``/totals``, ``/stats``, ``/downloadlist``.
"""

from __future__ import annotations

from typing import Any

from pydantic import RootModel

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = ["CurrentProfit", "DownloadItem", "StatsCache", "Total"]


class CurrentProfit(RainbowMinerModel):
    """Response of ``/currentprofit``.

    Attributes:
        AllProfitBTC: Combined profit (including remote miners) in BTC.
        ProfitBTC: Local profit in BTC.
        Earnings_Avg: Average earnings (local).
        Earnings_1d: 24-hour earnings (local).
        AllEarnings_Avg: Average earnings (including remote).
        AllEarnings_1d: 24-hour earnings (including remote).
        Rates: Current exchange rates used.
        PowerPrice: Current power price.
        Power: Current power draw — either a single number (watts) or a
            dict with ``CPU``, ``GPU``, and ``Offset`` keys.
        Uptime: RainbowMiner uptime.
        SysUptime: System uptime.
        RemoteIP: The server's remote IP — either a plain string or a dict
            containing geolocation data (``ip``, ``country``, etc.).
    """

    AllProfitBTC: float | int | None = None
    ProfitBTC: float | int | None = None
    Earnings_Avg: float | int | None = None
    Earnings_1d: float | int | None = None
    AllEarnings_Avg: float | int | None = None
    AllEarnings_1d: float | int | None = None
    Rates: dict[str, float | int] | None = None
    PowerPrice: float | int | None = None
    Power: float | int | dict[str, Any] | None = None
    Uptime: dict[str, Any] | None = None
    SysUptime: dict[str, Any] | None = None
    RemoteIP: str | dict[str, Any] | None = None


class Total(RainbowMinerModel):
    """An entry from ``/totals``."""


class StatsCache(RootModel[dict[str, Any]]):
    """Response of ``/stats`` — the stats cache (highly dynamic).

    Keys are stat identifiers (e.g. ``"CPU#Name_Algo_HashRate"``); values are
    objects with ``Live``, ``Day``, ``Week`` etc. fields.  Kept as a plain
    dict to remain forward-compatible across RainbowMiner versions.
    """


class DownloadItem(RainbowMinerModel):
    """An entry from ``/downloadlist`` — a queued or completed download."""
