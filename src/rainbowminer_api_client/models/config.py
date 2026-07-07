"""Models for config-related endpoints.

Covers: ``/config``, ``/userconfig``, ``/loadconfig``, ``/saveconfig``,
``/loadconfigjson``, ``/saveconfigjson``, ``/setup.json``.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, RootModel

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = [
    "Config",
    "LoadConfigJsonResult",
    "MinerConfig",
    "PoolsConfig",
    "SaveResult",
    "SetupJson",
    "UserConfig",
]


class Config(RootModel[dict[str, Any]]):
    """Response of ``/config`` — the merged running config (dynamic).

    The RainbowMiner config object has hundreds of keys and varies by version;
    it is exposed as a plain dict for maximum compatibility.
    """


class UserConfig(RootModel[dict[str, Any]]):
    """Response of ``/userconfig`` — user overrides of the config (dynamic)."""


class MinerConfig(RainbowMinerModel):
    """A single miner entry from ``/loadconfig?ConfigName=Miners``.

    Attributes:
        Name: Miner base name.
        Device: Target device.
        MainAlgorithm: Primary algorithm.
        SecondaryAlgorithm: Secondary algorithm (dual mining).
        Params: Extra miner command-line parameters.
        MSIAprofile: MSI Afterburner profile index.
        OCprofile: Overclock profile name.
        Difficulty: Pool difficulty override.
        Penalty: Profit penalty factor.
        Disable: Whether the miner is disabled.
        Tuning: Miner-specific tuning parameters.
    """

    Name: str = ""
    Device: str = ""
    MainAlgorithm: str = ""
    SecondaryAlgorithm: str = ""
    Params: str = ""
    MSIAprofile: str | None = None
    OCprofile: str | None = None
    Difficulty: str | None = None
    Penalty: float | int | str | None = None
    Disable: bool = False
    Tuning: dict[str, Any] | None = None


class PoolsConfig(RootModel[dict[str, Any]]):
    """Response of ``/loadconfig?ConfigName=Pools`` — pool config (dynamic)."""


class LoadConfigJsonResult(RainbowMinerModel):
    """Response of ``/loadconfigjson``.

    Attributes:
        Success: Whether the config file was read successfully.
        Data: The raw config file contents (JSON string).
    """

    Success: bool = False
    Data: str | None = None


class SaveResult(RainbowMinerModel):
    """Response of ``/saveconfig`` and ``/saveconfigjson``.

    Attributes:
        Success: Whether the config was saved.
        Data: Saved data echo (``saveconfig`` only).
    """

    Success: bool = False
    Data: dict[str, Any] | None = Field(default=None)


class SetupJson(RainbowMinerModel):
    """Response of ``/setup.json`` — aggregated setup config.

    Attributes:
        Autostart: Autostart configuration.
        Exclude: List of server config vars excluded from sync.
        Config: Main config object.
        Pools: Pools config object.
        Coins: Coins config object.
        OCProfiles: OC profiles config object.
        Scheduler: Scheduler config object.
        Userpools: Userpools config object.
    """

    Autostart: dict[str, Any] | None = None
    Exclude: list[str] = Field(default_factory=list)
    Config: Any | None = None
    Pools: Any | None = None
    Coins: Any | None = None
    OCProfiles: Any | None = None
    Scheduler: Any | None = None
    Userpools: Any | None = None
