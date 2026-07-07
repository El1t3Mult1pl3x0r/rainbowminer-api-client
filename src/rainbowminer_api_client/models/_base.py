"""Pydantic models for RainbowMiner API responses.

All models use ``extra="allow"`` so that new fields added by future
RainbowMiner versions do not break parsing.  Optional fields default to
``None`` or empty containers because the server frequently returns ``"[]"``
or ``null`` for endpoints with no data yet.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ["RainbowMinerModel"]


class RainbowMinerModel(BaseModel):
    """Base class for all RainbowMiner response models.

    Allows extra fields (forward-compatibility) and validates on assignment.
    """

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
