---
icon: lucide/download
description: Download CSV exports, debug ZIPs, and miner stats archives as binary responses.
---

# Binary endpoints

Some endpoints return binary data — CSV exports, ZIP archives — rather than JSON.
The client handles these via the `BinaryResponse` type, which wraps the raw
bytes alongside metadata.

## `BinaryResponse`

A `BinaryResponse` has three attributes:

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `.data` | `bytes` | Raw response body |
| `.content_type` | `str` | MIME type (e.g. `text/csv`, `application/zip`) |
| `.filename` | `str \| None` | Filename from the `Content-Disposition` header, if present |

## Endpoints

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_totals_csv()` | `/totalscsv` | `BinaryResponse` (CSV) | Totals as a CSV file |
| `get_earnings_csv()` | `/earnings?as_csv=true` | `BinaryResponse` (CSV) | Earnings as a CSV file |
| `save_miner_stats(miner_name=)` | `/saveminerstats` | `BinaryResponse` (ZIP) | Miner stats archive |
| `get_debug_zip()` | `/debug` | `BinaryResponse` (ZIP) | Debug information ZIP |

## Examples

### Save a CSV export to disk

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    csv = client.get_totals_csv()
    print(f"Content-Type: {csv.content_type}")
    print(f"Filename: {csv.filename}")

    with open("totals.csv", "wb") as f:
        f.write(csv.data)
    print("Saved totals.csv")
```

### Download a debug ZIP

```python
from rainbowminer_api_client import RainbowMinerClient


async with RainbowMinerClient("192.168.1.50", 4000) as client:
    debug = await client.get_debug_zip()
    print(f"Content-Type: {debug.content_type}")

    with open("debug.zip", "wb") as f:
        f.write(debug.data)
    print("Saved debug.zip")
```

### Save miner stats archive

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    stats = client.save_miner_stats(miner_name="Trex")
    filename = stats.filename or "miner_stats.zip"
    with open(filename, "wb") as f:
        f.write(stats.data)
    print(f"Saved {filename}")
```

## Next steps

- [:octicons-arrow-right-24: Monitoring endpoints](monitoring.md) — structured data endpoints
- [:octicons-arrow-right-24: API reference](../reference/client.md) — full method docs
