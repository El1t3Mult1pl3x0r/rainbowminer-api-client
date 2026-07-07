"""Models for console-related endpoints.

Covers: ``/console``.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = ["Console", "ConsoleMiner"]


class ConsoleMiner(RainbowMinerModel):
    """A running miner's log output inside a ``/console`` response.

    Attributes:
        Name: Display name (``"<DeviceModel> <BaseName>"``).
        Content: Tail of the miner's log file.
    """

    Name: str = ""
    Content: str = ""


class Console(RainbowMinerModel):
    """Response of ``/console``.

    Attributes:
        Content: The main console output (returns ``"*"`` when unchanged for
            the given ``ts``).
        Miners: Per-miner log tails for running miners.
        Timestamp: Unix timestamp of the console file's last write time.
        CmdMenu: Available command menu entries.
        CmdKey: Currently active command key.
    """

    Content: str = ""
    Miners: list[ConsoleMiner] = Field(default_factory=list)
    Timestamp: int = 0
    CmdMenu: list[Any] = Field(default_factory=list)
    CmdKey: str = ""
