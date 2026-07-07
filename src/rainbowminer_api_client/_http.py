"""Low-level HTTP transport for the RainbowMiner API client.

This module wraps :mod:`aiohttp` and exposes a small, typed interface used by
:class:`~rainbowminer_api_client.client.RainbowMinerClient`.  It handles base
URL construction, optional HTTP Basic authentication, timeouts, and mapping
HTTP status codes to the library's exception hierarchy.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import TracebackType
from typing import TYPE_CHECKING, Any

import aiohttp

from rainbowminer_api_client.errors import (
    RainbowMinerAPIError,
    RainbowMinerAuthError,
    RainbowMinerConnectionError,
    RainbowMinerNotFoundError,
)

if TYPE_CHECKING:
    from collections.abc import Collection

__all__ = ["BinaryResponse", "HttpTransport"]

_DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=30)


@dataclass(frozen=True, slots=True)
class BinaryResponse:
    """A non-JSON response body returned by binary endpoints (ZIP, CSV).

    Attributes:
        data: The raw response bytes.
        content_type: The ``Content-Type`` header value (e.g. ``application/zip``).
        filename: The filename suggested by the server via the
            ``Content-Disposition`` header, or ``None`` if not provided.
    """

    data: bytes
    content_type: str
    filename: str | None


class HttpTransport:
    """Async HTTP transport that talks to a single RainbowMiner server.

    The transport can either create its own :class:`aiohttp.ClientSession` or
    reuse an externally-managed one (useful in Home Assistant where a shared
    session is preferred).
    """

    def __init__(
        self,
        host: str,
        port: int,
        *,
        username: str | None = None,
        password: str | None = None,
        timeout: float | aiohttp.ClientTimeout = _DEFAULT_TIMEOUT,
        tls: bool = False,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Configure base URL, auth, and session management.

        Args:
            host: Hostname or IP address of the RainbowMiner server.
            port: TCP port the API server listens on (default ``4000``).
            username: Optional username for HTTP Basic auth.
            password: Optional password for HTTP Basic auth.
            timeout: Request timeout as total seconds, or an
                :class:`aiohttp.ClientTimeout` object.
            tls: If ``True``, use ``https://`` instead of ``http://``.
            session: An existing :class:`aiohttp.ClientSession` to reuse.  If
                ``None``, a session will be created on first use and closed by
                :meth:`close`.
        """
        scheme = "https" if tls else "http"
        self._base_url = f"{scheme}://{host}:{port}"
        self._auth_header: str | None = None
        if username is not None and password is not None:
            # aiohttp.encode_basic_auth already returns the full
            # "Basic <base64>" header value, so do not prepend "Basic ".
            self._auth_header = aiohttp.encode_basic_auth(username, password)
        self._timeout = aiohttp.ClientTimeout(total=timeout) if isinstance(timeout, float | int) else timeout
        self._session = session
        self._owns_session = session is None

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #
    async def close(self) -> None:
        """Close the internal session if it was created by this transport."""
        if self._owns_session and self._session is not None and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> HttpTransport:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    # ------------------------------------------------------------------ #
    # Session management
    # ------------------------------------------------------------------ #
    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Lazily create the aiohttp session if one was not provided."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    # ------------------------------------------------------------------ #
    # Public request helpers
    # ------------------------------------------------------------------ #
    async def get_json(
        self,
        path: str,
        *,
        params: Mapping[str, str | int | float | bool | None] | Collection[tuple[str, str]] | None = None,
    ) -> Any:
        """Perform a GET request and return the parsed JSON body.

        Args:
            path: Path component beginning with ``/`` (e.g. ``/stats``).
            params: Optional query parameters.  ``None`` values are skipped.

        Returns:
            The parsed JSON response (typically a dict or list).

        Raises:
            RainbowMinerConnectionError: Network/connectivity failure.
            RainbowMinerAuthError: HTTP 401.
            RainbowMinerNotFoundError: HTTP 404.
            RainbowMinerAPIError: Any other non-2xx status.
        """
        return await self._request_json("GET", path, params=params)

    async def post_json(
        self,
        path: str,
        *,
        params: Mapping[str, str | int | float | bool | None] | None = None,
        data: Mapping[str, str] | None = None,
    ) -> Any:
        """Perform a POST request and return the parsed JSON body.

        Args:
            path: Path component beginning with ``/``.
            params: Optional query parameters.  ``None`` values are skipped.
            data: Optional form-encoded body fields.

        Returns:
            The parsed JSON response.

        Raises:
            RainbowMinerConnectionError: Network/connectivity failure.
            RainbowMinerAuthError: HTTP 401.
            RainbowMinerNotFoundError: HTTP 404.
            RainbowMinerAPIError: Any other non-2xx status.
        """
        return await self._request_json("POST", path, params=params, data=data)

    async def get_binary(
        self,
        path: str,
        *,
        params: Mapping[str, str | int | float | bool | None] | None = None,
    ) -> BinaryResponse:
        """Perform a GET request and return the raw binary response.

        Args:
            path: Path component beginning with ``/``.
            params: Optional query parameters.  ``None`` values are skipped.

        Returns:
            A :class:`BinaryResponse` with the raw bytes, content type, and
            optional filename.

        Raises:
            RainbowMinerConnectionError: Network/connectivity failure.
            RainbowMinerAuthError: HTTP 401.
            RainbowMinerNotFoundError: HTTP 404.
            RainbowMinerAPIError: Any other non-2xx status.
        """
        return await self._request_binary("GET", path, params=params)

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #
    @staticmethod
    def _clean_params(
        params: Mapping[str, str | int | float | bool | None] | Collection[tuple[str, str]] | None,
    ) -> list[tuple[str, str]]:
        """Drop ``None`` values and stringify the rest for aiohttp."""
        if params is None:
            return []
        result: list[tuple[str, str]] = []
        if isinstance(params, Mapping):
            for k, v in params.items():
                if v is None:
                    continue
                result.append((str(k), _stringify(v)))
            return result
        return list(params)

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str | int | float | bool | None] | Collection[tuple[str, str]] | None = None,
        data: Mapping[str, str] | None = None,
    ) -> Any:
        """Issue a request expecting a JSON response."""
        url = self._base_url + path
        clean_params = self._clean_params(params)
        session = await self._ensure_session()
        try:
            headers = {"Authorization": self._auth_header} if self._auth_header else None
            async with session.request(
                method,
                url,
                params=clean_params,
                data=data,
                headers=headers,
            ) as resp:
                await self._raise_for_status(resp)
                # The RainbowMiner server always returns text (JSON-encoded
                # or plain text for some endpoints).  Parse JSON when possible.
                text = await resp.text()
        except aiohttp.ClientConnectorError as exc:
            raise RainbowMinerConnectionError(f"Cannot connect to {self._base_url}: {exc}") from exc
        except aiohttp.ClientError as exc:
            raise RainbowMinerConnectionError(str(exc)) from exc

        if not text:
            return None
        try:
            import json

            return json.loads(text)
        except json.JSONDecodeError, ValueError:
            # Not JSON — return the raw text so callers can handle it.
            return text

    async def _request_binary(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str | int | float | bool | None] | None = None,
    ) -> BinaryResponse:
        """Issue a request expecting a binary response."""
        url = self._base_url + path
        clean_params = self._clean_params(params)
        session = await self._ensure_session()
        try:
            headers = {"Authorization": self._auth_header} if self._auth_header else None
            async with session.request(method, url, params=clean_params, headers=headers) as resp:
                await self._raise_for_status(resp)
                data = await resp.read()
                content_type = resp.content_type
                filename = _filename_from_disposition(resp.headers.get("Content-Disposition", ""))
        except aiohttp.ClientConnectorError as exc:
            raise RainbowMinerConnectionError(f"Cannot connect to {self._base_url}: {exc}") from exc
        except aiohttp.ClientError as exc:
            raise RainbowMinerConnectionError(str(exc)) from exc

        return BinaryResponse(data=data, content_type=content_type, filename=filename)

    @staticmethod
    async def _raise_for_status(resp: aiohttp.ClientResponse) -> None:
        """Raise a library exception for non-2xx responses."""
        if resp.status < 400:
            return
        body = await resp.text()
        message = body.strip() or resp.reason or f"HTTP {resp.status}"
        if resp.status == 401:
            raise RainbowMinerAuthError(message)
        if resp.status == 404:
            raise RainbowMinerNotFoundError(message)
        raise RainbowMinerAPIError(message, status_code=resp.status)


def _stringify(value: Any) -> str:
    """Convert a scalar value to the string form expected by the API server."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _filename_from_disposition(header: str) -> str | None:
    """Extract the ``filename=`` portion from a Content-Disposition header.

    Args:
        header: The raw ``Content-Disposition`` header value.

    Returns:
        The filename if present, otherwise ``None``.
    """
    if not header:
        return None
    # Handles: attachment; filename=debug_2026-01-01.zip
    for part in header.split(";"):
        part = part.strip()
        if part.lower().startswith("filename="):
            return part.split("=", 1)[1].strip().strip('"')
    return None
