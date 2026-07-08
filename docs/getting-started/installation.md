---
icon: lucide/package
description: Install the RainbowMiner API client library.
---

# Installation

The RainbowMiner API client is published on [PyPI] and supports Python 3.14+.

  [PyPI]: https://pypi.org/project/rainbowminer-api-client/

## Requirements

!!! note "Prerequisites"

    - **Python 3.14 or newer**
    - A running [RainbowMiner] 4.x+ instance with the API server enabled
    - Network access to the RainbowMiner server's HTTP port (default: `4000`)

  [RainbowMiner]: https://github.com/RainbowMiner/RainbowMiner

## Install

=== "pip"

    ```bash
    pip install rainbowminer-api-client
    ```

=== "uv"

    ```bash
    uv add rainbowminer-api-client
    ```

=== "pipenv"

    ```bash
    pipenv install rainbowminer-api-client
    ```

## Dependencies

The library has minimal runtime dependencies:

| Package | Purpose |
| ------- | ------- |
| [`aiohttp`](https://docs.aiohttp.org/) | Async HTTP client |
| [`pydantic`](https://docs.pydantic.dev/) | Data validation and typed models |

Both are installed automatically when you install `rainbowminer-api-client`.

## Enable the RainbowMiner API

The RainbowMiner API server must be enabled in the RainbowMiner configuration:

1. Open your RainbowMiner `config.txt` (or use the web UI).
2. Set `APIs = 1` to enable the API server.
3. Set `APIport = 4000` (or your preferred port).
4. Optionally set `APIauth = 1` and configure `APIuser` / `APIpassword` for
   HTTP Basic authentication.

Restart RainbowMiner after changing these settings. Verify the API is
reachable:

```bash
curl http://192.168.1.50:4000/version
```

## Next steps

- [:octicons-arrow-right-24: Quick start](quick-start.md) — run your first request
