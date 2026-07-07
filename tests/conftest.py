"""Shared test fixtures for the rainbowminer_api_client test-suite.

A lightweight :mod:`aiohttp` test server mocks the RainbowMiner HTTP API.
Each endpoint path is mapped to a canned JSON response (or binary blob) so
tests can exercise the client without a live RainbowMiner instance.
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

import pytest
import pytest_aiohttp  # noqa: F401  -- registers async fixtures
from aiohttp import web

from rainbowminer_api_client import RainbowMinerClient, SyncRainbowMinerClient

# --------------------------------------------------------------------------- #
# Canned response data
# --------------------------------------------------------------------------- #

SAMPLE_VERSION = {"Version": "4.6.1.0", "VersionSort": "4.6.1.0", "VersionDate": "2026-01-01"}

SAMPLE_UPTIME = {"AsString": "1.02:03:04", "Seconds": 93784}

SAMPLE_IS_SERVER = {"Status": False}

SAMPLE_STATUS = {
    "Pause": False,
    "PauseIAOnly": False,
    "LockMiners": False,
    "IsExclusiveRun": False,
    "IsDonationRun": False,
}

SAMPLE_CURRENT_PROFIT = {
    "AllProfitBTC": 0.00123,
    "ProfitBTC": 0.00120,
    "Earnings_Avg": 0.00118,
    "Earnings_1d": 0.00115,
    "AllEarnings_Avg": 0.00123,
    "AllEarnings_1d": 0.00120,
    "Rates": {"BTC": 1.0, "USD": 65000.0},
    "PowerPrice": 0.12,
    "Power": 250.5,
    "Uptime": SAMPLE_UPTIME,
    "SysUptime": SAMPLE_UPTIME,
    "RemoteIP": None,
}

SAMPLE_ACTIVE_MINERS = [
    {"Name": "TRex-NVIDIA", "BaseName": "TRex", "DeviceName": ["GPU#0"], "BaseAlgorithm": ["Ethash"], "Speed": [120.5]},
]

SAMPLE_RUNNING_MINERS = [
    {"Name": "TRex-NVIDIA", "LogFile": "Logs\\1234_2026-01-01_00-00-00.txt"},
]

SAMPLE_POOLS = [
    {"Name": "2MinersEthash", "BaseName": "2Miners", "Currency": "ETH", "Balance": 0.01},
]

SAMPLE_BALANCES = [
    {"Name": "2MinersETH", "BaseName": "2Miners", "Currency": "ETH", "Total": 0.01, "Paid": 0.5, "Earnings": 0.001},
]

SAMPLE_PAYOUTS = [
    {"Name": "2MinersETH", "Currency": "ETH", "Date": "2026-01-01 12:00:00", "Amount": 0.5, "Txid": "abc123"},
]

SAMPLE_EARNINGS = {
    "total": 2,
    "totalNotFiltered": 2,
    "rows": [
        {
            "Date": "2026-01-01 12:00:00",
            "Date_UTC": "2026-01-01 12:00:00",
            "PoolName": "2MinersETH",
            "Currency": "ETH",
            "Balance": 0.01,
            "Paid": 0.5,
            "Earnings": 0.001,
            "Value": 65.0,
        },
    ],
}

SAMPLE_RATES = {"BTC": 1.0, "USD": 65000.0, "ETH": 32.0}

SAMPLE_DEVICES = [
    {"Type": "Gpu", "Vendor": "NVIDIA", "Model": "RTX 3080", "Name": "GPU#0"},
]

SAMPLE_OC_PROFILES = [
    {
        "Name": "Profile1",
        "Device": "GPU#0",
        "PowerLimit": 200,
        "ThermalLimit": 80,
        "MemoryClockBoost": 500,
        "CoreClockBoost": 100,
    },
]

SAMPLE_MRR_STATS = [
    {"Algorithm": "Ethash", "Title": "Ethash", "SuggPrice": 0.001, "LastPrice": 0.0009, "HashRate": 120.5},
]

SAMPLE_TOGGLE_RESULT = {"Status": True, "Disabled": True}

SAMPLE_SAVE_RESULT = {"Success": True}

SAMPLE_LOAD_CONFIG_JSON = {"Success": True, "Data": '{"WorkerName":"test"}'}

SAMPLE_CONSOLE = {
    "Content": "RainbowMiner starting...",
    "Miners": [],
    "Timestamp": 1234567890,
    "CmdMenu": [],
    "CmdKey": "",
}

SAMPLE_CPU_INFO = {"Cores": 8, "Threads": 16, "Name": "AMD Ryzen 7"}

SAMPLE_MRR_CONTROL = [
    {"Name": "Ethash", "PriceFactor": 1.0, "Algorithms": ["Ethash"], "LastReset": "2026-01-01 00:00:00"},
]

CSV_DATA = b"Pool,Profit\r\n2MinersETH,0.001\r\n"

ZIP_DATA = b"PK\x03\x04" + b"\x00" * 20

# --------------------------------------------------------------------------- #
# Mock server routes
# --------------------------------------------------------------------------- #

# Type alias for the handler registry: path → callable returning response body.
RouteHandler = Callable[[web.Request], Awaitable[Any]]

# Default JSON routes — path → canned JSON body.
JSON_ROUTES: dict[str, Any] = {
    "/version": SAMPLE_VERSION,
    "/info": {"MachineName": "TestRig"},
    "/remoteip": None,
    "/console": SAMPLE_CONSOLE,
    "/cpuinfo": SAMPLE_CPU_INFO,
    "/sysinfo": {"OS": "Linux"},
    "/uptime": SAMPLE_UPTIME,
    "/systemuptime": SAMPLE_UPTIME,
    "/isserver": SAMPLE_IS_SERVER,
    "/activeminers": SAMPLE_ACTIVE_MINERS,
    "/runningminers": SAMPLE_RUNNING_MINERS,
    "/failedminers": [],
    "/remoteminers": [],
    "/minersneedingbenchmark": [],
    "/minerinfo": [],
    "/minerspeeds": [],
    "/pools": SAMPLE_POOLS,
    "/allpools": SAMPLE_POOLS,
    "/newpools": [],
    "/algorithms": ["Ethash"],
    "/miners": [],
    "/fastestminers": [],
    "/availminers": ["TRex", "TeamRedMiner"],
    "/availminerstats": [{"Name": "TRex", "Statcount": 5}],
    "/disabled": ["TRex-Ethash"],
    "/getwtmurls": {"GPU#0": "https://whattomine.com/coins?..."},
    "/loadconfigjson": SAMPLE_LOAD_CONFIG_JSON,
    "/loadconfig": {"WorkerName": "test"},
    "/config": {"WorkerName": "test"},
    "/userconfig": {"WorkerName": "test"},
    "/ocprofiles": SAMPLE_OC_PROFILES,
    "/downloadlist": [],
    "/alldevices": SAMPLE_DEVICES,
    "/devices": SAMPLE_DEVICES,
    "/platforms": {},
    "/devicecombos": [],
    "/getdeviceconfig": [{"Name": "CPU", "Selected": True, "Excluded": False}],
    "/stats": {"CPU#Test_Ethash_HashRate": {"Live": 100, "Day": 95}},
    "/totals": [],
    "/sessionvars": {"WorkerName": "test"},
    "/session": {"WorkerName": "test"},
    "/gc": {},
    "/watchdogtimers": [],
    "/crashcounter": [],
    "/payouts": SAMPLE_PAYOUTS,
    "/rates": SAMPLE_RATES,
    "/asyncloaderjobs": [],
    "/decsep": ".",
    "/getminerlog": {"Status": False, "Content": ""},
    "/minerstats": [],
    "/computerstats": {"CPU": 50.0, "GPU": [70.0]},
    "/minerports": {"TRex": 4001},
    "/currentprofit": SAMPLE_CURRENT_PROFIT,
    "/status": SAMPLE_STATUS,
    "/clients": [],
    "/mrrstats": SAMPLE_MRR_STATS,
    "/mrrrigs": [],
    "/mrrcontrol": SAMPLE_MRR_CONTROL,
    "/setup.json": {
        "Autostart": {"Enable": "0"},
        "Exclude": [],
        "Config": {},
        "Pools": {},
        "Coins": {},
        "OCProfiles": {},
        "Scheduler": {},
        "Userpools": {},
    },
}

# Endpoints that return plain text (not JSON).
TEXT_ROUTES: dict[str, str] = {
    "/stop": "Stopping",
    "/reboot": "Reboot is disabled.",
    "/applyoc": "Please wait, OC will be applied asap",
    "/resetworkers": "No valid MinerStatusKey found in config.txt",
}

# Boolean-returning endpoints (JSON-encoded true/false).
BOOL_ROUTES: dict[str, bool] = {
    "/pause": True,
    "/lockminers": False,
    "/update": True,
    "/updatebalance": True,
    "/updatemrr": True,
    "/watchdogreset": True,
}

# Binary routes — path → (bytes, content_type, filename).
BINARY_ROUTES: dict[str, tuple[bytes, str, str]] = {
    "/totalscsv": (CSV_DATA, "text/csv", "totals_2026-01-01_120000.txt"),
    "/saveminerstats": (ZIP_DATA, "application/zip", "minerstats-all-2026-01-01.zip"),
    "/debug": (ZIP_DATA, "application/zip", "debug_2026-01-01.zip"),
}

# Write endpoints that return JSON — path → canned JSON body.
WRITE_JSON_ROUTES: dict[str, Any] = {
    "/cmdkey": "a",
    "/saveconfigjson": SAMPLE_SAVE_RESULT,
    "/saveconfig": SAMPLE_SAVE_RESULT,
    "/action/toggleminer": SAMPLE_TOGGLE_RESULT,
    "/action/togglepool": SAMPLE_TOGGLE_RESULT,
}


def _build_mock_app() -> web.Application:
    """Build the aiohttp test application with all mock routes.

    Returns:
        A configured :class:`web.Application` with all endpoints registered.
    """
    app = web.Application()

    async def json_handler(request: web.Request, body: Any) -> web.Response:
        """Return a JSON response for the given canned body."""
        return web.json_response(body)

    async def text_handler(request: web.Request, body: str) -> web.Response:
        """Return a plain-text response."""
        return web.Response(text=body, content_type="text/html")

    async def bool_handler(request: web.Request, body: bool) -> web.Response:
        """Return a JSON-encoded boolean."""
        return web.Response(text=json.dumps(body), content_type="application/json")

    async def binary_handler(request: web.Request, data: bytes, ct: str, filename: str) -> web.Response:
        """Return a binary response with Content-Disposition header."""
        return web.Response(
            body=data,
            content_type=ct,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    # Earnings needs special handling for the paginated response + CSV mode.
    async def earnings_handler(request: web.Request) -> web.Response:
        """Handle /earnings with optional as_csv query param."""
        if request.query.get("as_csv"):
            return web.Response(body=CSV_DATA, content_type="text/csv")
        return web.json_response(SAMPLE_EARNINGS)

    # Balances needs special handling for as_csv mode.
    async def balances_handler(request: web.Request) -> web.Response:
        """Handle /balances with optional as_csv query param."""
        if request.query.get("as_csv"):
            return web.Response(body=CSV_DATA, content_type="text/csv")
        return web.json_response(SAMPLE_BALANCES)

    # Activity needs special handling for as_csv mode.
    async def activity_handler(request: web.Request) -> web.Response:
        """Handle /activity with optional as_csv query param."""
        if request.query.get("as_csv"):
            return web.Response(body=CSV_DATA, content_type="text/csv")
        return web.json_response([])

    # Register all JSON routes.
    for path, body in JSON_ROUTES.items():
        app.router.add_get(path, lambda req, b=body: json_handler(req, b))

    # Register text routes.
    for path, body in TEXT_ROUTES.items():
        app.router.add_get(path, lambda req, b=body: text_handler(req, b))

    # Register boolean routes.
    for path, body in BOOL_ROUTES.items():
        app.router.add_get(path, lambda req, b=body: bool_handler(req, b))

    # Register binary routes.
    for path, (data, ct, filename) in BINARY_ROUTES.items():
        app.router.add_get(path, lambda req, d=data, c=ct, f=filename: binary_handler(req, d, c, f))

    # Register write endpoints (accept GET and POST).
    for path, body in WRITE_JSON_ROUTES.items():
        app.router.add_get(path, lambda req, b=body: json_handler(req, b))
        app.router.add_post(path, lambda req, b=body: json_handler(req, b))

    # Special handlers.
    app.router.add_get("/earnings", earnings_handler)
    app.router.add_get("/balances", balances_handler)
    app.router.add_get("/activity", activity_handler)

    return app


# --------------------------------------------------------------------------- #
# Pytest fixtures
# --------------------------------------------------------------------------- #


@pytest.fixture()
async def aiohttp_app() -> web.Application:
    """Provide the mock aiohttp application.

    Returns:
        The mock :class:`web.Application` with all test routes.
    """
    return _build_mock_app()


# A persistent test server that stays running for the duration of the test.
# Both the async client and the sync client connect to it independently.
@pytest.fixture()
async def test_server() -> Any:
    """Start a persistent aiohttp test server with all mock routes."""
    from aiohttp.test_utils import TestServer

    server = TestServer(_build_mock_app())
    await server.start_server()
    yield server
    await server.close()


@pytest.fixture()
async def client(test_server: Any) -> Any:
    """Provide an async RainbowMinerClient pointed at the mock server."""
    rbm_client = RainbowMinerClient(host="127.0.0.1", port=test_server.port)
    yield rbm_client
    await rbm_client.close()


@pytest.fixture()
async def sync_server() -> Any:
    """Start a standard-library HTTP server in a background thread."""
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    # Build a combined route map for quick lookup.
    all_routes: dict[str, Any] = {}
    all_routes.update(JSON_ROUTES)
    all_routes.update(TEXT_ROUTES)
    all_routes.update(BOOL_ROUTES)
    all_routes.update(WRITE_JSON_ROUTES)
    # Binary routes
    binary_map = {p: (d, c, f) for p, (d, c, f) in BINARY_ROUTES.items()}

    class MockHandler(BaseHTTPRequestHandler):
        """Minimal HTTP handler that serves canned responses."""

        def _handle(self) -> None:
            """Serve a canned response based on the request path."""
            path = self.path.split("?")[0]

            # Check special endpoints first.
            if path == "/earnings":
                if "as_csv=true" in self.path.split("?", 1)[-1] if "?" in self.path else "":
                    self._send_binary(CSV_DATA, "text/csv", "earnings.csv")
                else:
                    self._send_json(SAMPLE_EARNINGS)
                return
            if path == "/balances":
                if "as_csv=true" in self.path.split("?", 1)[-1] if "?" in self.path else "":
                    self._send_binary(CSV_DATA, "text/csv", "balances.csv")
                else:
                    self._send_json(SAMPLE_BALANCES)
                return
            if path == "/activity":
                if "as_csv=true" in self.path.split("?", 1)[-1] if "?" in self.path else "":
                    self._send_binary(CSV_DATA, "text/csv", "activities.csv")
                else:
                    self._send_json([])
                return

            # Check binary routes.
            if path in binary_map:
                data, ct, filename = binary_map[path]
                self._send_binary(data, ct, filename)
                return

            # Check other routes.
            body = all_routes.get(path)
            if body is None:
                self.send_response(404)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"Not found")
                return
            if isinstance(body, bool):
                self._send_text(json.dumps(body), "application/json")
            elif isinstance(body, str):
                self._send_text(body, "text/html")
            else:
                self._send_json(body)

        def do_GET(self) -> None:
            """Handle GET requests."""
            self._handle()

        def do_POST(self) -> None:
            """Handle POST requests."""
            self._handle()

        def _send_json(self, body: Any) -> None:
            """Send a JSON response."""
            self._send_text(json.dumps(body), "application/json")

        def _send_text(self, text: str, content_type: str) -> None:
            """Send a plain-text response."""
            data = text.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _send_binary(self, data: bytes, ct: str, filename: str) -> None:
            """Send a binary response with Content-Disposition."""
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: Any) -> None:
            """Suppress log output during tests."""
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield port
    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture()
async def sync_client(sync_server: Any) -> Any:
    """Provide a SyncRainbowMinerClient pointed at the mock server."""
    import threading

    port = sync_server
    result_holder: list[SyncRainbowMinerClient] = []
    error_holder: list[Exception] = []

    def _construct() -> None:
        """Create the sync client in a thread with its own event loop."""
        try:
            sc = SyncRainbowMinerClient(host="127.0.0.1", port=port)
            result_holder.append(sc)
        except Exception as e:
            error_holder.append(e)

    t = threading.Thread(target=_construct)
    t.start()
    t.join()

    if error_holder:
        raise error_holder[0]

    sc = result_holder[0]
    yield sc
    # Close the sync client (and its aiohttp session) after the test.
    # close() must be called from a separate thread because it uses
    # run_until_complete() which conflicts with the running pytest-asyncio loop.
    close_holder: list[Exception] = []

    def _close() -> None:
        """Close the sync client in its own thread."""
        try:
            sc.close()
        except Exception as e:
            close_holder.append(e)

    ct = threading.Thread(target=_close)
    ct.start()
    ct.join()
    if close_holder:
        raise close_holder[0]
