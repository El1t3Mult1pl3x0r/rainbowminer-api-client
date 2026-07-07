"""Models for miscellaneous endpoints.

Covers: ``/clients``, ``/disabled``, ``/getwtmurls``, ``/action/toggleminer``,
``/action/togglepool``, ``/downloadlist``, ``/rates``.
"""

from __future__ import annotations

from pydantic import RootModel

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = [
    "Client",
    "RateTableRow",
    "RatesDict",
    "ToggleResult",
    "WtmUrls",
]


class Client(RainbowMinerModel):
    """An entry from ``/clients`` — a connected RainbowMiner client.

    Attributes:
        workername: Worker name.
        machinename: Machine name.
        machineip: Machine IP address.
        port: API port.
        timestamp: Last-seen Unix timestamp.
        isserver: ``True`` for the server entry itself.
    """

    workername: str | None = None
    machinename: str | None = None
    machineip: str | None = None
    port: int | None = None
    timestamp: int | None = None
    isserver: bool = False


class WtmUrls(RootModel[dict[str, str]]):
    """Response of ``/getwtmurls`` — device-model → WhatToMine URL mapping."""


class ToggleResult(RainbowMinerModel):
    """Response of ``/action/toggleminer`` and ``/action/togglepool``.

    Attributes:
        Status: Whether the request was well-formed.
        Disabled: ``True`` if the resource is now disabled, ``False`` if
            re-enabled.  Absent when ``Status`` is ``False``.
    """

    Status: bool = False
    Disabled: bool | None = None


class RatesDict(RootModel[dict[str, float | int]]):
    """Response of ``/rates`` (default) — currency → rate mapping."""


class RateTableRow(RainbowMinerModel):
    """A row from ``/rates?format=table``.

    Attributes:
        symbol: Currency symbol.
    """

    symbol: str = ""

    def rate(self, currency: str) -> float | int | None:
        """Get the exchange rate for a given currency.

        Args:
            currency: The currency symbol (e.g. ``"USD"``).

        Returns:
            The rate value, or ``None`` if not present in this row.
        """
        val: float | int | None
        try:
            raw = getattr(self, f"rate{currency}")
            val = float(raw) if raw is not None else None
        except AttributeError:
            val = None
        return val
