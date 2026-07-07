"""Exception hierarchy for the RainbowMiner API client.

All exceptions raised by the client derive from :class:`RainbowMinerError` so
callers can catch any library-specific error with a single ``except`` clause.
"""

from __future__ import annotations

__all__ = [
    "RainbowMinerAPIError",
    "RainbowMinerAuthError",
    "RainbowMinerConnectionError",
    "RainbowMinerError",
    "RainbowMinerNotFoundError",
]


class RainbowMinerError(Exception):
    """Base exception for all RainbowMiner API client errors."""


class RainbowMinerConnectionError(RainbowMinerError):
    """Raised when the client cannot connect to the RainbowMiner API server."""


class RainbowMinerAuthError(RainbowMinerError):
    """Raised when the API server rejects the request with HTTP 401 Unauthorized."""


class RainbowMinerNotFoundError(RainbowMinerError):
    """Raised when the API server returns HTTP 404 for the requested resource."""


class RainbowMinerAPIError(RainbowMinerError):
    """Raised for any non-2xx HTTP status not covered by a more specific error.

    Attributes:
        status_code: The HTTP status code returned by the server.
    """

    def __init__(self, message: str, *, status_code: int) -> None:
        """Store the HTTP status code alongside the error message.

        Args:
            message: Human-readable description of the error.
            status_code: The HTTP status code returned by the server.
        """
        super().__init__(message)
        self.status_code = status_code
