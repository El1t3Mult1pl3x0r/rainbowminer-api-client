---
icon: lucide/rocket
description: Get up and running with the RainbowMiner API client in minutes.
---

# Quick start

This guide walks through the most common usage patterns: async, sync, and
authenticated access to a RainbowMiner server.

!!! tip "Prerequisites"

    Make sure you've [installed](installation.md) the library and your
    RainbowMiner API server is [enabled and reachable](installation.md#enable-the-rainbowminer-api).

## Async usage

The `RainbowMinerClient` is async-first, built on `aiohttp`. It's designed for
integration with Home Assistant and other async Python applications.

```python
import asyncio

from rainbowminer_api_client import RainbowMinerClient


async def main() -> None:
    # Use as an async context manager — the connection is automatically closed
    async with RainbowMinerClient("192.168.1.50", 4000) as client:
        # Check the current profit
        profit = await client.get_current_profit()
        print(f"Current profit: {profit.ProfitBTC} BTC")

        # List active miners
        miners = await client.get_active_miners()
        for miner in miners:
            print(f"  {miner.Name}: {miner.Speed}")

        # Get server status
        status = await client.get_status()
        print(f"Paused: {status.Pause}")


asyncio.run(main())
```

!!! info "Context manager"

    The client supports `async with` to ensure the underlying `aiohttp`
    session is properly closed. You can also manage the lifecycle manually with
    `await client.connect()` and `await client.close()`.

## Sync usage

For scripts, CLI tools, or any non-async context, use `SyncRainbowMinerClient`.
It wraps the async client with a private event loop — you never need to touch
`asyncio.run()`.

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    profit = client.get_current_profit()
    print(f"Current profit: {profit.ProfitBTC} BTC")

    miners = client.get_active_miners()
    for miner in miners:
        print(f"  {miner.Name}: {miner.Speed}")
```

## With authentication

RainbowMiner uses HTTP Basic auth when `APIauth` is enabled in the
configuration:

```python
from rainbowminer_api_client import RainbowMinerClient


# Async with authentication
async with RainbowMinerClient(
    "192.168.1.50",
    4000,
    username="admin",
    password="secret",
) as client:
    status = await client.get_status()
    print(f"Paused: {status.Pause}")
```

For the sync client:

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient(
    "192.168.1.50",
    4000,
    username="admin",
    password="secret",
) as client:
    status = client.get_status()
    print(f"Paused: {status.Pause}")
```

!!! warning "Auth header format"

    The library uses `aiohttp.encode_basic_auth` internally, which produces the
    full `"Basic <base64>"` header. The library handles this correctly — you
    just pass `username` and `password`.

## Constructor parameters

| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `host` | `str` | _(required)_ | RainbowMiner server hostname or IP |
| `port` | `int` | `4000` | RainbowMiner API port |
| `username` | `str \| None` | `None` | HTTP Basic auth username |
| `password` | `str \| None` | `None` | HTTP Basic auth password |
| `timeout` | `float` | `30` | Request timeout in seconds |
| `verify_ssl` | `bool` | `False` | Whether to verify SSL certificates |

## Next steps

- [:octicons-arrow-right-24: Monitoring endpoints](../guide/monitoring.md) — full endpoint reference
- [:octicons-arrow-right-24: Control endpoints](../guide/control.md) — pause, reboot, toggle
- [:octicons-arrow-right-24: API reference](../reference/client.md) — auto-generated docs
