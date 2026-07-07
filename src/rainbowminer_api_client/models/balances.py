"""Models for balance, payout, and earnings endpoints.

Covers: ``/balances``, ``/payouts``, ``/earnings``.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = ["Balance", "Earning", "EarningsResult", "Payout"]


class Balance(RainbowMinerModel):
    """An entry from ``/balances``.

    Attributes:
        Name: Balance entry name (pool or wallet name).
        BaseName: Base name (``"TotalPools"``, ``"Wallet"``, etc.).
        Currency: Currency symbol.
        Started: Tracking start timestamp.
        Total: Current unpaid balance.
        Paid: Total amount paid out.
        Earnings: Total earnings.
        Earnings_1h: Earnings in the last hour.
        Earnings_1d: Earnings in the last day.
        Earnings_1w: Earnings in the last week.
        Earnings_Avg: Average earnings.
    """

    Name: str | None = None
    BaseName: str | None = None
    Currency: str | None = None
    Started: str | None = None
    Total: float | int | str | None = None
    Paid: float | int | str | None = None
    Earnings: float | int | str | None = None
    Earnings_1h: float | int | str | None = None
    Earnings_1d: float | int | str | None = None
    Earnings_1w: float | int | str | None = None
    Earnings_Avg: float | int | str | None = None
    Total_BTC: float | int | str | None = None
    Paid_BTC: float | int | str | None = None
    Earnings_BTC: float | int | str | None = None
    Earnings_1h_BTC: float | int | str | None = None
    Earnings_1d_BTC: float | int | str | None = None
    Earnings_1w_BTC: float | int | str | None = None
    Earnings_Avg_BTC: float | int | str | None = None
    Last_Earnings: Any | None = None
    Payouts: Any | None = None


class Payout(RainbowMinerModel):
    """An entry from ``/payouts``.

    Attributes:
        Name: Pool base name.
        Currency: Currency symbol.
        Date: Payout timestamp.
        Amount: Payout amount.
        Txid: Transaction ID.
    """

    Name: str | None = None
    Currency: str | None = None
    Date: str | None = None
    Amount: float | int | None = None
    Txid: str | None = None


class Earning(RainbowMinerModel):
    """An entry from ``/earnings``.

    Attributes:
        Date: Local timestamp.
        Date_UTC: UTC timestamp.
        PoolName: Pool name.
        Currency: Currency symbol.
        Balance: Current balance.
        Paid: Total paid.
        Earnings: Earnings for the period.
        Value: Fiat value.
        Balance_BTC: Balance in BTC.
        Paid_BTC: Paid in BTC.
        Earnings_BTC: Earnings in BTC.
        Value_BTC: Fiat value in BTC.
    """

    Date: str | None = None
    Date_UTC: str | None = None
    PoolName: str | None = None
    Currency: str | None = None
    Balance: float | int | None = None
    Paid: float | int | None = None
    Earnings: float | int | None = None
    Value: float | int | None = None
    Balance_BTC: float | int | None = None
    Paid_BTC: float | int | None = None
    Earnings_BTC: float | int | None = None
    Value_BTC: float | int | None = None


class EarningsResult(RainbowMinerModel):
    """Paginated response of ``/earnings``.

    Attributes:
        total: Number of rows after filtering.
        totalNotFiltered: Number of rows before filtering.
        rows: The requested page of earnings.
    """

    total: int = 0
    totalNotFiltered: int = 0
    rows: list[Earning] = Field(default_factory=list)
