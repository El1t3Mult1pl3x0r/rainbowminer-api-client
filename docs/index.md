---
title: RainbowMiner API Client
description: A typed Python API client for RainbowMiner — monitor and control your multipool cryptominer from Python.
---

# RainbowMiner API Client

A typed Python API client for [RainbowMiner], the multipool cryptominer. This
library provides a clean, async-first interface to monitor and control a
RainbowMiner server from Python applications — including [Home Assistant]
integrations.

The client is a **pure communication interface**: it sends HTTP requests to the
RainbowMiner local API and parses the responses into typed Pydantic models. It
does not execute anything on the RainbowMiner server itself.

  [RainbowMiner]: https://github.com/RainbowMiner/RainbowMiner
  [Home Assistant]: https://www.home-assistant.io/

---

## Features

<div class="grid cards" markdown>

-   :material-language-python:__Async-first__

    ---

    Built on `aiohttp` — ideal for Home Assistant and other async Python
    applications. Full async/await support with connection pooling.

-   :material-sync:__Sync wrapper__

    ---

    `SyncRainbowMinerClient` provides a blocking interface for scripts and
    non-async callers — no `asyncio.run()` needed.

-   :material-shield-check:__Fully typed__

    ---

    Pydantic v2 models for every endpoint, with `py.typed` (PEP 561) marker.
    Full type annotations on all public APIs.

-   :material-eye:__Monitoring__

    ---

    Miners, pools, balances, earnings, profit, devices, stats, activity, and
    more — all parsed into structured models.

-   :material-toggle-switch:__Control__

    ---

    Pause, stop, reboot, update, toggle miner/pool, save config — full remote
    control of your RainbowMiner instance.

-   :material-alert-circle:__Error hierarchy__

    ---

    Typed exceptions for auth, connection, and API errors. Catch library
    errors with a single `except` clause or handle specific cases.

</div>

---

## Quick install

=== "pip"

    ```bash
    pip install rainbowminer-api-client
    ```

=== "uv"

    ```bash
    uv add rainbowminer-api-client
    ```

---

## Quick start

### Async _(recommended for Home Assistant)_

```python
import asyncio

from rainbowminer_api_client import RainbowMinerClient


async def main() -> None:
    async with RainbowMinerClient("192.168.1.50", 4000) as client:
        profit = await client.get_current_profit()
        print(f"Current profit: {profit.ProfitBTC} BTC")

        miners = await client.get_active_miners()
        for miner in miners:
            print(f"  {miner.Name}: {miner.Speed}")


asyncio.run(main())
```

### Sync _(for scripts and non-async apps)_

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    profit = client.get_current_profit()
    print(f"Current profit: {profit.ProfitBTC} BTC")
```

### With authentication

```python
from rainbowminer_api_client import RainbowMinerClient


# RainbowMiner uses HTTP Basic auth when APIauth is enabled
async with RainbowMinerClient(
    "192.168.1.50",
    4000,
    username="admin",
    password="secret",
) as client:
    status = await client.get_status()
    print(f"Paused: {status.Pause}")
```

---

## Explore

<div class="grid cards" markdown>

-   :material-book-open-variant:__Getting started__

    ---

    Install the client and run your first request in minutes.

    [:octicons-arrow-right-24: Installation](getting-started/installation.md)

-   :material-rocket-launch:__Quick start__

    ---

    Walk through async, sync, and authenticated usage examples.

    [:octicons-arrow-right-24: Quick start](getting-started/quick-start.md)

-   :material-eye:__Monitoring endpoints__

    ---

    Browse all monitoring endpoints with return types and examples.

    [:octicons-arrow-right-24: Monitoring](guide/monitoring.md)

-   :material-toggle-switch:__Control endpoints__

    ---

    Pause, reboot, toggle miners, save config, and more.

    [:octicons-arrow-right-24: Control](guide/control.md)

-   :material-code-braces:__API reference__

    ---

    Auto-generated reference for every class, method, and model.

    [:octicons-arrow-right-24: RainbowMinerClient](reference/client.md)

-   :material-alert-circle:__Error handling__

    ---

    Exception hierarchy and practical error-handling strategies.

    [:octicons-arrow-right-24: Error handling](guide/error-handling.md)

</div>
