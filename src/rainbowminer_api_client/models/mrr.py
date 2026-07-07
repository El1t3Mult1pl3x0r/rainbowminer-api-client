"""Models for MiningRigRentals (MRR) endpoints.

Covers: ``/mrrstats``, ``/mrrrigs``, ``/mrrcontrol``.
"""

from __future__ import annotations

from typing import Any

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = ["MrrControl", "MrrRig", "MrrStat"]


class MrrStat(RainbowMinerModel):
    """An entry from ``/mrrstats`` — algorithm-level MRR statistics.

    Attributes:
        Algorithm: MRR algorithm name.
        Title: Display title.
        SuggPrice: Suggested price.
        LastPrice: Last traded price.
        RigsPrice: Estimated rig price.
        Unit: Hashrate unit.
        Hot: Whether the algorithm is "hot".
        RigsAvail: Number of available rigs.
        RigsRented: Number of rented rigs.
        HashRate: Local hashrate for this algorithm.
    """

    Algorithm: str | None = None
    Title: str | None = None
    SuggPrice: float | int | None = None
    LastPrice: float | int | None = None
    RigsPrice: float | int | None = None
    Unit: str | None = None
    Hot: bool = False
    RigsAvail: int | None = None
    RigsRented: int | None = None
    HashRate: float | int | None = None


class MrrRig(RainbowMinerModel):
    """An entry from ``/mrrrigs`` — per-rig MRR data.

    Attributes:
        Algorithm: MRR algorithm name.
        Title: Display title.
        Price: Current BTC price.
        MinPrice: Minimum BTC price.
        Modifier: Price modifier.
        Multiplier: Unit multiplier.
        MinHours: Minimum rental hours.
        MaxHours: Maximum rental hours.
        HashRate: Local hashrate.
        HashRateAdv: Advertised hashrate.
    """

    Algorithm: str | None = None
    Title: str | None = None
    Price: float | int | None = None
    MinPrice: float | int | None = None
    Modifier: float | int | None = None
    Multiplier: float | int | None = None
    MinHours: int | None = None
    MaxHours: int | None = None
    HashRate: float | int | None = None
    HashRateAdv: float | int | None = None


class MrrControl(RainbowMinerModel):
    """An entry from ``/mrrcontrol``.

    Attributes:
        Name: Controller name.
        PriceFactor: Price factor applied.
        Algorithms: Algorithms under control.
        LastReset: Last reset timestamp.
    """

    Name: str | None = None
    PriceFactor: float | int | None = None
    Algorithms: list[Any] | None = None
    LastReset: str | None = None
