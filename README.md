# rainbowminer-api-client

[![PyPI version](https://img.shields.io/pypi/v/rainbowminer-api-client.svg)](https://pypi.org/project/rainbowminer-api-client/)
[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A typed Python API client for [RainbowMiner](https://github.com/RainbowMiner/RainbowMiner), the multipool cryptominer. This library provides a clean, async-first interface to monitor and control a RainbowMiner server from Python applications — including [Home Assistant](https://www.home-assistant.io/) integrations.

📚 **[Documentation](https://el1t3mult1pl3x0r.github.io/rainbowminer-api-client/)**

The client is a **pure communication interface**: it sends HTTP requests to the RainbowMiner local API and parses the responses into typed Pydantic models. It does not execute anything on the RainbowMiner server itself.

## Features

- **Async-first** with `aiohttp` — ideal for Home Assistant and other async Python apps
- **Sync wrapper** (`SyncRainbowMinerClient`) for non-async callers — no `asyncio.run()` needed
- **Fully typed** — Pydantic v2 models for every endpoint, with `py.typed` (PEP 561) marker
- **Monitoring endpoints** — miners, pools, balances, earnings, profit, devices, stats, activity
- **Control endpoints** — pause, stop, reboot, update, toggle miner/pool, save config
- **Binary endpoints** — download debug ZIPs, miner stats archives, CSV exports
- **Error hierarchy** — typed exceptions for auth, connection, and API errors

## Installation

```bash
pip install rainbowminer-api-client
```

## Quick start

### Async (recommended for Home Assistant)

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

### Sync (for scripts and non-async apps)

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
async with RainbowMinerClient("192.168.1.50", 4000, username="admin", password="secret") as client:
    status = await client.get_status()
    print(f"Paused: {status.Pause}")
```

## Monitoring endpoints

All methods are async on `RainbowMinerClient` and sync on `SyncRainbowMinerClient`.

| Method | Endpoint | Returns |
| ------ | -------- | ------- |
| `get_version()` | `/version` | `Version` |
| `get_info()` | `/info` | `Any` |
| `get_current_profit()` | `/currentprofit` | `CurrentProfit` |
| `get_status()` | `/status` | `Status` |
| `is_server()` | `/isserver` | `bool` |
| `get_remote_ip()` | `/remoteip` | `str \| None` |
| `get_console(ts=)` | `/console` | `Console` |
| `get_cpu_info()` | `/cpuinfo` | `CPUInfo` |
| `get_sys_info()` | `/sysinfo` | `SysInfo` |
| `get_uptime()` | `/uptime` | `Uptime` |
| `get_system_uptime()` | `/systemuptime` | `Uptime` |
| `get_active_miners()` | `/activeminers` | `list[ActiveMiner]` |
| `get_running_miners()` | `/runningminers` | `list[RunningMiner]` |
| `get_failed_miners()` | `/failedminers` | `list[FailedMiner]` |
| `get_remote_miners(mode=)` | `/remoteminers` | `list[RemoteMiner] \| list[RemoteMinerEntry]` |
| `get_miners_needing_benchmark()` | `/minersneedingbenchmark` | `list[Any]` |
| `get_miner_info()` | `/minerinfo` | `list[MinerInfo]` |
| `get_miner_speeds()` | `/minerspeeds` | `list[MinerSpeed]` |
| `get_miners()` | `/miners` | `list[Miner]` |
| `get_fastest_miners()` | `/fastestminers` | `list[FastestMiner]` |
| `get_avail_miners()` | `/availminers` | `list[str]` |
| `get_avail_miner_stats()` | `/availminerstats` | `list[AvailMinerStat]` |
| `get_disabled()` | `/disabled` | `list[str]` |
| `get_algorithms()` | `/algorithms` | `list[str]` |
| `get_pools()` | `/pools` | `list[Pool]` |
| `get_all_pools()` | `/allpools` | `list[AllPool]` |
| `get_new_pools()` | `/newpools` | `list[NewPool]` |
| `get_balances(...)` | `/balances` | `list[Balance] \| BinaryResponse` |
| `get_payouts()` | `/payouts` | `list[Payout]` |
| `get_earnings(...)` | `/earnings` | `EarningsResult` |
| `get_rates(format=)` | `/rates` | `dict[str, float] \| list[RateTableRow]` |
| `get_all_devices()` | `/alldevices` | `list[AllDevice]` |
| `get_devices()` | `/devices` | `list[Device]` |
| `get_platforms()` | `/platforms` | `dict[str, Any]` |
| `get_device_combos()` | `/devicecombos` | `list[DeviceCombo]` |
| `get_device_config()` | `/getdeviceconfig` | `list[DeviceConfigEntry]` |
| `get_oc_profiles()` | `/ocprofiles` | `list[OCProfile]` |
| `get_download_list()` | `/downloadlist` | `list[DownloadItem]` |
| `get_stats()` | `/stats` | `dict[str, Any]` |
| `get_totals()` | `/totals` | `list[Total]` |
| `get_activity(as_csv=)` | `/activity` | `list[Any] \| BinaryResponse` |
| `get_computer_stats()` | `/computerstats` | `ComputerStats` |
| `get_miner_stats()` | `/minerstats` | `list[MinerStat]` |
| `get_miner_log(logfile=)` | `/getminerlog` | `MinerLogResult` |
| `get_miner_ports()` | `/minerports` | `dict[str, Any]` |
| `get_config()` | `/config` | `Config` |
| `get_user_config()` | `/userconfig` | `UserConfig` |
| `load_config(config_name=, pool_name=)` | `/loadconfig` | `Any` |
| `load_config_json(config_name=)` | `/loadconfigjson` | `LoadConfigJsonResult` |
| `get_wtm_urls()` | `/getwtmurls` | `dict[str, str]` |
| `get_session_vars()` | `/sessionvars` | `dict[str, Any]` |
| `get_session()` | `/session` | `dict[str, Any]` |
| `get_gc()` | `/gc` | `dict[str, Any]` |
| `get_watchdog_timers()` | `/watchdogtimers` | `list[Any]` |
| `get_crash_counter()` | `/crashcounter` | `list[Any]` |
| `get_asyncloader_jobs()` | `/asyncloaderjobs` | `list[AsyncloaderJob]` |
| `get_dec_sep()` | `/decsep` | `str` |
| `get_clients(include_server=)` | `/clients` | `list[Client]` |
| `get_mrr_stats()` | `/mrrstats` | `list[MrrStat]` |
| `get_mrr_rigs()` | `/mrrrigs` | `list[MrrRig]` |
| `get_mrr_control()` | `/mrrcontrol` | `list[MrrControl]` |
| `get_setup()` | `/setup.json` | `SetupJson` |

## Control endpoints

| Method | Endpoint | Returns |
| ------ | -------- | ------- |
| `pause(action=...)` | `/pause` | `bool` |
| `stop()` | `/stop` | `str` |
| `reboot()` | `/reboot` | `str` |
| `update()` | `/update` | `bool` |
| `update_balance()` | `/updatebalance` | `bool` |
| `update_mrr()` | `/updatemrr` | `bool` |
| `lock_miners()` | `/lockminers` | `bool` |
| `reset_workers()` | `/resetworkers` | `str` |
| `apply_oc()` | `/applyoc` | `str` |
| `watchdog_reset()` | `/watchdogreset` | `bool` |
| `set_cmd_key(cmd_key=)` | `/cmdkey` | `str` |
| `toggle_miner(name=, algorithm=, device_model=)` | `/action/toggleminer` | `ToggleResult` |
| `toggle_pool(name=, algorithm=, coin_symbol=)` | `/action/togglepool` | `ToggleResult` |
| `save_config(config_name=, **fields)` | `/saveconfig` | `SaveResult` |
| `save_config_json(config_name=, data=)` | `/saveconfigjson` | `SaveResult` |

## Binary endpoints

| Method | Endpoint | Returns |
| ------ | -------- | ------- |
| `get_totals_csv()` | `/totalscsv` | `BinaryResponse` (CSV) |
| `get_earnings_csv()` | `/earnings?as_csv=true` | `BinaryResponse` (CSV) |
| `save_miner_stats(miner_name=)` | `/saveminerstats` | `BinaryResponse` (ZIP) |
| `get_debug_zip()` | `/debug` | `BinaryResponse` (ZIP) |

`BinaryResponse` has `.data` (bytes), `.content_type` (str), and `.filename` (str | None).

## Sync / async parity

Every public async method on `RainbowMinerClient` has a corresponding sync method on `SyncRainbowMinerClient` with the same name and signature. This parity is enforced by an automated test. When a new async method is added, the sync counterpart is added in the same change.

## Error handling

All exceptions derive from `RainbowMinerError`:

```python
from rainbowminer_api_client import RainbowMinerError, RainbowMinerAuthError, RainbowMinerConnectionError

try:
    profit = await client.get_current_profit()
except RainbowMinerAuthError:
    print("Authentication failed — check your username/password")
except RainbowMinerConnectionError:
    print("Cannot connect to RainbowMiner — is it running?")
except RainbowMinerError as e:
    print(f"API error: {e}")
```

## Compatibility

- Python 3.14+
- RainbowMiner 4.x+ (API server must be enabled in config)

## License

[MIT](LICENSE)
