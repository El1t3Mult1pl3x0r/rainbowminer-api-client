"""Tests for the :class:`RainbowMinerClient` construction, auth, and error mapping."""

from __future__ import annotations

from typing import Any

import pytest

from rainbowminer_api_client import (
    RainbowMinerAPIError,
    RainbowMinerAuthError,
    RainbowMinerClient,
    RainbowMinerConnectionError,
    RainbowMinerNotFoundError,
)
from rainbowminer_api_client._http import HttpTransport


class TestConstruction:
    """Tests for client construction and defaults."""

    def test_default_host_port(self) -> None:
        """Client should default to localhost:4000."""
        client = RainbowMinerClient()
        assert client._transport._base_url == "http://localhost:4000"

    def test_custom_host_port(self) -> None:
        """Client should accept custom host and port."""
        client = RainbowMinerClient("192.168.1.50", 8080)
        assert client._transport._base_url == "http://192.168.1.50:8080"

    def test_tls(self) -> None:
        """Client should use https:// when tls=True."""
        client = RainbowMinerClient("example.com", 443, tls=True)
        assert client._transport._base_url == "https://example.com:443"

    def test_auth_configured(self) -> None:
        """Client should configure Basic auth when username/password provided."""
        client = RainbowMinerClient("host", 4000, username="user", password="pass")
        assert client._transport._auth_header is not None
        assert client._transport._auth_header.startswith("Basic ")

    def test_no_auth_by_default(self) -> None:
        """Client should not configure auth when no credentials provided."""
        client = RainbowMinerClient()
        assert client._transport._auth_header is None


class TestHttpTransport:
    """Tests for the low-level HTTP transport param cleaning."""

    def test_clean_params_drops_none(self) -> None:
        """_clean_params should drop None values."""
        transport = HttpTransport("localhost", 4000)
        result = transport._clean_params({"a": "1", "b": None, "c": 2})
        assert ("a", "1") in result
        assert ("c", "2") in result
        assert not any(k == "b" for k, _ in result)

    def test_clean_params_bools(self) -> None:
        """_clean_params should stringify booleans as 'true'/'false'."""
        transport = HttpTransport("localhost", 4000)
        result = transport._clean_params({"flag": True, "off": False})
        assert ("flag", "true") in result
        assert ("off", "false") in result

    def test_clean_params_none_input(self) -> None:
        """_clean_params should return an empty list for None input."""
        transport = HttpTransport("localhost", 4000)
        assert transport._clean_params(None) == []


class TestErrorMapping:
    """Tests for HTTP status code → exception mapping."""

    @pytest.mark.usefixtures("aiohttp_client")
    async def test_401_raises_auth_error(self, aiohttp_client: Any) -> None:
        """HTTP 401 should raise RainbowMinerAuthError."""
        from aiohttp import web

        app = web.Application()

        async def unauthorized(_request: web.Request) -> web.Response:
            return web.Response(status=401, text="Access denied")

        app.router.add_get("/version", unauthorized)
        test_client = await aiohttp_client(app)
        client = RainbowMinerClient(host="127.0.0.1", port=test_client.port)
        client._transport._session = test_client.session
        client._transport._owns_session = False

        with pytest.raises(RainbowMinerAuthError):
            await client.get_version()

    @pytest.mark.usefixtures("aiohttp_client")
    async def test_404_raises_not_found_error(self, aiohttp_client: Any) -> None:
        """HTTP 404 should raise RainbowMinerNotFoundError."""
        from aiohttp import web

        app = web.Application()

        async def not_found(_request: web.Request) -> web.Response:
            return web.Response(status=404, text="Not found")

        app.router.add_get("/version", not_found)
        test_client = await aiohttp_client(app)
        client = RainbowMinerClient(host="127.0.0.1", port=test_client.port)
        client._transport._session = test_client.session
        client._transport._owns_session = False

        with pytest.raises(RainbowMinerNotFoundError):
            await client.get_version()

    @pytest.mark.usefixtures("aiohttp_client")
    async def test_500_raises_api_error(self, aiohttp_client: Any) -> None:
        """HTTP 500 should raise RainbowMinerAPIError with status_code."""
        from aiohttp import web

        app = web.Application()

        async def server_error(_request: web.Request) -> web.Response:
            return web.Response(status=500, text="Internal error")

        app.router.add_get("/version", server_error)
        test_client = await aiohttp_client(app)
        client = RainbowMinerClient(host="127.0.0.1", port=test_client.port)
        client._transport._session = test_client.session
        client._transport._owns_session = False

        with pytest.raises(RainbowMinerAPIError) as exc_info:
            await client.get_version()
        assert exc_info.value.status_code == 500


class TestTimeoutHandling:
    """Tests for timeout propagation and TimeoutError mapping in HttpTransport."""

    @pytest.mark.usefixtures("aiohttp_client")
    async def test_timeout_passed_to_shared_session_request(self, aiohttp_client: Any) -> None:
        """session.request must receive the configured timeout when a shared session is used."""
        from unittest.mock import patch

        from aiohttp import web

        app = web.Application()

        async def ok(_request: web.Request) -> web.Response:
            return web.json_response({"Version": "1.0"})

        app.router.add_get("/version", ok)
        test_client = await aiohttp_client(app)
        client = RainbowMinerClient(host="127.0.0.1", port=test_client.port, timeout=5.0)
        client._transport._session = test_client.session
        client._transport._owns_session = False

        captured_kwargs: dict[str, Any] = {}
        original_request = test_client.session.request

        # aiohttp's session.request returns a _RequestContextManager (not a
        # coroutine), so the spy must be a plain function that delegates and
        # returns that same object — not an async function.
        def spy_request(*args: Any, **kwargs: Any) -> Any:
            captured_kwargs.update(kwargs)
            return original_request(*args, **kwargs)

        with patch.object(test_client.session, "request", side_effect=spy_request):
            await client.get_version()

        assert "timeout" in captured_kwargs
        assert captured_kwargs["timeout"] == client._transport._timeout
        assert captured_kwargs["timeout"].total == 5.0

    async def test_timeout_error_mapped_to_connection_error(self, test_server: Any) -> None:
        """A raw TimeoutError from session.request should be wrapped in RainbowMinerConnectionError."""
        from unittest.mock import AsyncMock, MagicMock, patch

        client = RainbowMinerClient(host="127.0.0.1", port=test_server.port)
        # session.request is a regular call returning an async context manager;
        # raise TimeoutError immediately when it is called.  Must use MagicMock
        # (not AsyncMock) so the exception fires before `async with` evaluates.
        mock_session = MagicMock()
        mock_session.request.side_effect = TimeoutError("simulated timeout")
        mock_ensure = AsyncMock(return_value=mock_session)

        with (
            patch.object(client._transport, "_ensure_session", mock_ensure),
            pytest.raises(RainbowMinerConnectionError, match="Timeout"),
        ):
            await client.get_version()

        await client.close()
