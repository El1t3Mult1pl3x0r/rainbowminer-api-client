---
icon: lucide/refresh-cw
description: Understand the relationship between the async and sync clients.
---

# Sync / async parity

The library provides two clients with identical APIs:

- **`RainbowMinerClient`** — async-first, built on `aiohttp`
- **`SyncRainbowMinerClient`** — blocking wrapper around the async client

Every public async method on `RainbowMinerClient` has a corresponding sync
method on `SyncRainbowMinerClient` with the **same name and signature** (minus
`async`/`await`). This parity is enforced by an automated test — when a new
async method is added, the sync counterpart is added in the same change.

## Which should I use?

| Use case | Client |
| -------- | ------ |
| Home Assistant integration | `RainbowMinerClient` (async) |
| Any `asyncio` application | `RainbowMinerClient` (async) |
| CLI scripts | `SyncRainbowMinerClient` (sync) |
| Jupyter notebooks | `SyncRainbowMinerClient` (sync) |
| Existing synchronous codebase | `SyncRainbowMinerClient` (sync) |

## Side-by-side comparison

=== "Async"

    ```python
    import asyncio

    from rainbowminer_api_client import RainbowMinerClient


    async def main() -> None:
        async with RainbowMinerClient("192.168.1.50", 4000) as client:
            profit = await client.get_current_profit()
            print(f"Profit: {profit.ProfitBTC} BTC")


    asyncio.run(main())
    ```

=== "Sync"

    ```python
    from rainbowminer_api_client import SyncRainbowMinerClient


    with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
        profit = client.get_current_profit()
        print(f"Profit: {profit.ProfitBTC} BTC")
    ```

## How the sync client works

`SyncRainbowMinerClient` owns a private `asyncio` event loop and an internal
`RainbowMinerClient` instance. Each sync method call runs the corresponding
async method on that private loop, so callers never need to touch
`asyncio.run()`.

This means:

- **No event loop conflicts** — the sync client manages its own loop, so it
  works inside environments that already have a running loop (though you'd
  typically use the async client in those cases).
- **Same error types** — both clients raise the same `RainbowMinerError`
  hierarchy.
- **Same models** — both return the same Pydantic model types.

## Parity enforcement

Parity is enforced by `tests/test_sync_client.py`. If you add a new async
method to `RainbowMinerClient`, add the sync counterpart to
`SyncRainbowMinerClient` in the same change — the test will fail otherwise.

## Next steps

- [:octicons-arrow-right-24: API reference — RainbowMinerClient](../reference/client.md)
- [:octicons-arrow-right-24: API reference — SyncRainbowMinerClient](../reference/sync-client.md)
