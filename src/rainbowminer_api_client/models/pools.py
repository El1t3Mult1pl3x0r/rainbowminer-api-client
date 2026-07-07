"""Models for pool-related endpoints.

Covers: ``/pools``, ``/allpools``, ``/newpools``, ``/algorithms``.
"""

from __future__ import annotations

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = ["Algorithm", "AllPool", "NewPool", "Pool"]


class Pool(RainbowMinerModel):
    """An entry from ``/pools`` (currently active/enabled pools).

    Attributes:
        Name: Pool name.
        BaseName: Pool base name.
        Algorithm: Algorithm(s) the pool is mining.
        Currency: Payout currency symbol.
        Balance: Current unpaid balance.
        Paid: Total paid out.
        Earnings: Recent earnings.
    """

    Name: str | None = None
    BaseName: str | None = None
    Algorithm: list[str] | str | None = None
    Currency: str | None = None
    Balance: float | int | None = None
    Paid: float | int | None = None
    Earnings: float | int | None = None


class AllPool(RainbowMinerModel):
    """An entry from ``/allpools`` (all known pools, active or not)."""


class NewPool(RainbowMinerModel):
    """An entry from ``/newpools`` (newly discovered pools)."""


class Algorithm(RainbowMinerModel):
    """An entry from ``/algorithms``."""
