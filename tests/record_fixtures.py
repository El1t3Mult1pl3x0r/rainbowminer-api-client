"""Record live RainbowMiner API responses to JSON fixtures.

This script connects to a real RainbowMiner server, fetches every read-only
endpoint listed in :mod:`tests.fixture_registry`, and saves the raw JSON
response to ``tests/fixtures/real/<name>.json``.  The resulting fixtures are
then replayed by :mod:`tests.test_replay_fixtures` to validate that the
Pydantic models match the upstream API contract.

Usage (from the project root):

    uv run python -m tests.record_fixtures --host 192.168.1.50 --port 4000

Optional arguments:

    --username <user> --password <pass>   HTTP Basic auth credentials.
    --tls                                 Use https:// instead of http://.
    --outdir tests/fixtures/real          Override the output directory.
    --overwrite                           Overwrite existing fixture files.

The script is **read-only** — it never calls any endpoint that mutates
server state.  Only endpoints listed in
``tests.fixture_registry.READ_ONLY_ENDPOINTS`` are fetched.

Exit code 0 means all fixtures were recorded; non-zero means at least one
endpoint failed (details printed per endpoint).
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

import aiohttp

from tests.fixture_registry import READ_ONLY_ENDPOINTS, EndpointSpec

DEFAULT_OUTDIR = Path(__file__).resolve().parent / "fixtures" / "real"


class NotFoundError(Exception):
    """Raised when a read-only endpoint returns 404 (data not yet available)."""

    def __init__(self, path: str) -> None:
        """Store the endpoint path that returned 404.

        Args:
            path: The API path that returned 404.
        """
        self.path = path
        super().__init__(f"404 Not Found for {path}")


async def _fetch(session: aiohttp.ClientSession, base_url: str, spec: EndpointSpec) -> Any:
    """Fetch one endpoint and return the decoded JSON, or raise.

    A 404 is re-raised as :class:`NotFoundError` so the caller can decide
    whether to treat it as "no data yet" (common for endpoints backed by
    ``$API.*`` fields that are still ``$null``) or a real failure.
    """
    url = f"{base_url}{spec.path}"
    params = {k: v for k, v in (spec.params or {}).items() if v is not None}
    async with session.get(url, params=params or None) as resp:
        if resp.status == 404:
            raise NotFoundError(spec.path)
        resp.raise_for_status()
        text = await resp.text()
        if not text:
            return None
        return json.loads(text)


async def record(
    host: str,
    port: int,
    *,
    username: str | None = None,
    password: str | None = None,
    tls: bool = False,
    outdir: Path = DEFAULT_OUTDIR,
    overwrite: bool = False,
) -> int:
    """Record all read-only endpoints to ``outdir``.

    Args:
        host: RainbowMiner server hostname.
        port: RainbowMiner API port.
        username: Optional HTTP Basic auth username.
        password: Optional HTTP Basic auth password.
        tls: If ``True``, use ``https://``.
        outdir: Directory to write fixture JSON files to.
        overwrite: If ``True``, overwrite existing fixtures.

    Returns:
        The number of endpoints that failed to record (0 = all OK).
    """
    scheme = "https" if tls else "http"
    base_url = f"{scheme}://{host}:{port}"
    outdir.mkdir(parents=True, exist_ok=True)

    headers: dict[str, str] = {}
    if username is not None and password is not None:
        # aiohttp.encode_basic_auth returns the full "Basic <base64>" value.
        headers["Authorization"] = aiohttp.encode_basic_auth(username, password)
    timeout = aiohttp.ClientTimeout(total=30)
    failures = 0

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        for spec in READ_ONLY_ENDPOINTS:
            dest = outdir / f"{spec.name}.json"
            if dest.exists() and not overwrite:
                print(f"SKIP  {spec.name:30s}  (exists; use --overwrite)")
                continue
            try:
                data = await _fetch(session, base_url, spec)
            except NotFoundError as exc:
                # 404 means the endpoint exists but the backing data is not
                # available on this rig (e.g. $API.ComputerStats is still
                # $null).  Record a null fixture so the replay test still
                # exercises the model's empty/null path.
                dest.write_text("null\n")
                print(f"EMPTY {spec.name:30s}  {spec.path}  -> {exc}")
                continue
            except Exception as exc:
                failures += 1
                print(f"FAIL  {spec.name:30s}  {spec.path}  -> {exc}")
                continue
            dest.write_text(json.dumps(data, indent=2, sort_keys=True, default=str) + "\n")
            print(f"OK    {spec.name:30s}  {spec.path}")

    print(f"\nRecorded {len(READ_ONLY_ENDPOINTS) - failures}/{len(READ_ONLY_ENDPOINTS)} endpoints to {outdir}")
    return failures


def main() -> None:
    """Parse CLI args and run the recording loop."""
    parser = argparse.ArgumentParser(description="Record live RainbowMiner API fixtures.")
    parser.add_argument("--host", default="localhost", help="RainbowMiner server host")
    parser.add_argument("--port", type=int, default=4000, help="RainbowMiner API port")
    parser.add_argument("--username", default=None, help="HTTP Basic auth username")
    parser.add_argument("--password", default=None, help="HTTP Basic auth password")
    parser.add_argument("--tls", action="store_true", help="Use HTTPS")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR, help="Output directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing fixtures")
    args = parser.parse_args()

    failures = asyncio.run(
        record(
            host=args.host,
            port=args.port,
            username=args.username,
            password=args.password,
            tls=args.tls,
            outdir=args.outdir,
            overwrite=args.overwrite,
        )
    )
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
