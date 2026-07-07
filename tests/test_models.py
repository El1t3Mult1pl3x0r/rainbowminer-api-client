"""Tests for Pydantic model parsing edge cases.

RainbowMiner endpoints often return ``"[]"``, ``null``, or objects with
missing/extra fields.  These tests verify that models handle those cases
gracefully.
"""

from __future__ import annotations

from rainbowminer_api_client.models.balances import Balance, EarningsResult, Payout
from rainbowminer_api_client.models.common import Status, Uptime, Version
from rainbowminer_api_client.models.devices import Device
from rainbowminer_api_client.models.miners import ActiveMiner
from rainbowminer_api_client.models.misc import ToggleResult
from rainbowminer_api_client.models.pools import Pool
from rainbowminer_api_client.models.profit import CurrentProfit


class TestEmptyAndNull:
    """Models should handle empty arrays, null, and missing fields."""

    def test_version_minimal(self) -> None:
        """Version should parse with only one field present."""
        v = Version.model_validate({"Version": "1.0"})
        assert v.Version == "1.0"
        assert v.Build is None

    def test_uptime_missing_seconds(self) -> None:
        """Uptime should parse with missing Seconds field (defaults to 0)."""
        u = Uptime.model_validate({"AsString": "0.00:00:01"})
        assert u.AsString == "0.00:00:01"
        assert u.Seconds == 0

    def test_status_all_missing(self) -> None:
        """Status should parse with all fields missing."""
        s = Status.model_validate({})
        assert s.Pause is False
        assert s.LockMiners is False

    def test_current_profit_all_missing(self) -> None:
        """CurrentProfit should parse with all fields missing."""
        cp = CurrentProfit.model_validate({})
        assert cp.ProfitBTC is None
        assert cp.Rates is None

    def test_balance_minimal(self) -> None:
        """Balance should parse with only Name and Currency."""
        b = Balance.model_validate({"Name": "Test", "Currency": "ETH"})
        assert b.Name == "Test"
        assert b.Currency == "ETH"
        assert b.Total is None

    def test_payout_minimal(self) -> None:
        """Payout should parse with minimal fields."""
        p = Payout.model_validate({"Name": "Test", "Currency": "ETH"})
        assert p.Name == "Test"

    def test_earnings_result_empty(self) -> None:
        """EarningsResult should default to empty rows and zero totals."""
        e = EarningsResult.model_validate({})
        assert e.total == 0
        assert e.totalNotFiltered == 0
        assert e.rows == []

    def test_earnings_result_null(self) -> None:
        """EarningsResult should handle null input gracefully."""
        # The client wraps null in EarningsResult() so this just tests the default.
        e = EarningsResult()
        assert e.rows == []

    def test_toggle_result_minimal(self) -> None:
        """ToggleResult should parse with only Status=False."""
        t = ToggleResult.model_validate({"Status": False})
        assert t.Status is False
        assert t.Disabled is None


class TestExtraFieldsAllowed:
    """Models with extra='allow' should accept unknown fields without error."""

    def test_version_extra_field(self) -> None:
        """Version should accept unknown fields."""
        v = Version.model_validate({"Version": "1.0", "UnknownField": "value"})
        assert v.Version == "1.0"

    def test_active_miner_extra_field(self) -> None:
        """ActiveMiner should accept unknown fields."""
        m = ActiveMiner.model_validate({"Name": "TRex", "NewField": 42})
        assert m.Name == "TRex"

    def test_current_profit_extra_field(self) -> None:
        """CurrentProfit should accept unknown fields."""
        cp = CurrentProfit.model_validate({"ProfitBTC": 0.001, "Future": True})
        assert cp.ProfitBTC == 0.001

    def test_pool_extra_field(self) -> None:
        """Pool should accept unknown fields."""
        p = Pool.model_validate({"Name": "Test", "Extra": [1, 2, 3]})
        assert p.Name == "Test"

    def test_device_extra_field(self) -> None:
        """Device should accept unknown fields."""
        d = Device.model_validate({"Type": "Gpu", "New": "x"})
        assert d.Type == "Gpu"


class TestNumericFlexibility:
    """Models should accept int or float for numeric fields interchangeably."""

    def test_current_profit_int_profit(self) -> None:
        """CurrentProfit should accept int for ProfitBTC."""
        cp = CurrentProfit.model_validate({"ProfitBTC": 0})
        assert cp.ProfitBTC == 0

    def test_current_profit_float_profit(self) -> None:
        """CurrentProfit should accept float for ProfitBTC."""
        cp = CurrentProfit.model_validate({"ProfitBTC": 0.00123})
        assert cp.ProfitBTC == 0.00123

    def test_current_profit_power_dict(self) -> None:
        """CurrentProfit should accept a dict for Power (CPU/GPU/Offset)."""
        cp = CurrentProfit.model_validate({"Power": {"CPU": 154.08, "GPU": 0.0, "Offset": 0.0}})
        assert cp.Power == {"CPU": 154.08, "GPU": 0.0, "Offset": 0.0}

    def test_current_profit_power_number(self) -> None:
        """CurrentProfit should accept a plain number for Power."""
        cp = CurrentProfit.model_validate({"Power": 250.5})
        assert cp.Power == 250.5

    def test_current_profit_remote_ip_dict(self) -> None:
        """CurrentProfit should accept a dict for RemoteIP (geolocation)."""
        remote_ip = {"ip": "2a10:3781:92:1:be24:11ff:fe00:b262", "country": {"code": "NL", "name": "The Netherlands"}}
        cp = CurrentProfit.model_validate({"RemoteIP": remote_ip})
        assert cp.RemoteIP == remote_ip

    def test_current_profit_remote_ip_string(self) -> None:
        """CurrentProfit should accept a plain string for RemoteIP."""
        cp = CurrentProfit.model_validate({"RemoteIP": "203.0.113.5"})
        assert cp.RemoteIP == "203.0.113.5"

    def test_uptime_int_seconds(self) -> None:
        """Uptime should accept int for Seconds."""
        u = Uptime.model_validate({"Seconds": 100})
        assert u.Seconds == 100

    def test_uptime_float_seconds(self) -> None:
        """Uptime should coerce float to int for Seconds."""
        u = Uptime.model_validate({"Seconds": 100.0})
        assert u.Seconds == 100
