---
icon: lucide/toggle-right
description: Control your RainbowMiner — pause, stop, reboot, update, toggle miners, and save config.
---

# Control endpoints

The client provides methods to control a RainbowMiner server remotely. All
methods are async on `RainbowMinerClient` and sync on `SyncRainbowMinerClient`.

!!! warning "Side effects"

    Control endpoints change the state of your RainbowMiner server. Use them
    with care — especially `stop()`, `reboot()`, and `update()`.

## Server control

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `pause(action=...)` | `/pause` | `bool` | Pause or resume mining |
| `stop()` | `/stop` | `str` | Stop all miners |
| `reboot()` | `/reboot` | `str` | Reboot the RainbowMiner server |
| `update()` | `/update` | `bool` | Trigger a RainbowMiner self-update |

### Pause

`pause()` accepts an optional `action` parameter:

```python
from rainbowminer_api_client import RainbowMinerClient


async with RainbowMinerClient("192.168.1.50", 4000) as client:
    # Pause mining
    result = await client.pause(action="pause")
    print(f"Paused: {result}")

    # Resume mining
    result = await client.pause(action="resume")
    print(f"Resumed: {result}")

    # Toggle pause state (default)
    result = await client.pause()
```

### Stop, reboot, update

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    # Stop all miners
    result = client.stop()
    print(result)

    # Reboot the RainbowMiner server
    result = client.reboot()
    print(result)

    # Trigger self-update
    updating = client.update()
    print(f"Updating: {updating}")
```

## Maintenance

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `update_balance()` | `/updatebalance` | `bool` | Refresh balance data |
| `update_mrr()` | `/updatemrr` | `bool` | Refresh MRR data |
| `lock_miners()` | `/lockminers` | `bool` | Lock miners from switching |
| `reset_workers()` | `/resetworkers` | `str` | Reset worker stats |
| `apply_oc()` | `/applyoc` | `str` | Apply overclock profiles |
| `watchdog_reset()` | `/watchdogreset` | `bool` | Reset the watchdog |
| `set_cmd_key(cmd_key=)` | `/cmdkey` | `str` | Set a command key |

## Toggle miner / pool

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `toggle_miner(name=, algorithm=, device_model=)` | `/action/toggleminer` | `ToggleResult` | Enable/disable a miner |
| `toggle_pool(name=, algorithm=, coin_symbol=)` | `/action/togglepool` | `ToggleResult` | Enable/disable a pool |

### Example: Toggle a miner

```python
from rainbowminer_api_client import RainbowMinerClient


async with RainbowMinerClient("192.168.1.50", 4000) as client:
    result = await client.toggle_miner(
        name="Trex",
        algorithm="autolykos2",
        device_model="NVIDIA RTX 3070",
    )
    print(f"Success: {result.Success}")
```

### Example: Toggle a pool

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    result = client.toggle_pool(
        name="2Miners",
        algorithm="autolykos2",
        coin_symbol="ERG",
    )
    print(f"Success: {result.Success}")
```

## Save config

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `save_config(config_name=, **fields)` | `/saveconfig` | `SaveResult` | Save config fields |
| `save_config_json(config_name=, data=)` | `/saveconfigjson` | `SaveResult` | Save full config JSON |

### Example: Save a config value

```python
from rainbowminer_api_client import RainbowMinerClient


async with RainbowMinerClient("192.168.1.50", 4000) as client:
    result = await client.save_config(
        config_name="default",
        APIport=4001,
    )
    print(f"Saved: {result.Success}")
```

### Example: Save full config JSON

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    result = client.save_config_json(
        config_name="backup",
        data={"APIport": 4001, "APIs": 1},
    )
    print(f"Saved: {result.Success}")
```

## Next steps

- [:octicons-arrow-right-24: Binary endpoints](binary.md) — CSV/ZIP downloads
- [:octicons-arrow-right-24: API reference](../reference/client.md) — full method docs
