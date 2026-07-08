---
icon: lucide/eye
description: Monitor your RainbowMiner instance — miners, pools, balances, devices, stats, and more.
---

# Monitoring endpoints

The client provides typed methods for every RainbowMiner monitoring endpoint.
All methods are async on `RainbowMinerClient` and sync on
`SyncRainbowMinerClient` — they share the same names and signatures.

## Server & system

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_version()` | `/version` | `Version` | RainbowMiner version info |
| `get_info()` | `/info` | `Any` | General server information |
| `get_current_profit()` | `/currentprofit` | `CurrentProfit` | Current profit across all miners |
| `get_status()` | `/status` | `Status` | Server status (paused, running, etc.) |
| `is_server()` | `/isserver` | `bool` | Whether this instance is a server |
| `get_remote_ip()` | `/remoteip` | `str \| None` | Remote IP of the client |
| `get_console(ts=)` | `/console` | `Console` | Console output with optional timestamp filter |
| `get_cpu_info()` | `/cpuinfo` | `CPUInfo` | CPU information |
| `get_sys_info()` | `/sysinfo` | `SysInfo` | System information |
| `get_uptime()` | `/uptime` | `Uptime` | RainbowMiner uptime |
| `get_system_uptime()` | `/systemuptime` | `Uptime` | Operating system uptime |
| `get_computer_stats()` | `/computerstats` | `ComputerStats` | CPU/GPU temps, load, memory |

### Example: Current profit

```python
from rainbowminer_api_client import RainbowMinerClient


async with RainbowMinerClient("192.168.1.50", 4000) as client:
    profit = await client.get_current_profit()
    print(f"BTC: {profit.ProfitBTC}")
    print(f"USD: {profit.ProfitUSD}")
    print(f"EUR: {profit.ProfitEUR}")
```

### Example: System info

```python
from rainbowminer_api_client import SyncRainbowMinerClient


with SyncRainbowMinerClient("192.168.1.50", 4000) as client:
    sysinfo = client.get_sys_info()
    print(f"OS: {sysinfo.OSName} {sysinfo.OSVersion}")
    print(f"CPU: {sysinfo.CPUName}")

    cpu = client.get_cpu_info()
    print(f"CPU load: {cpu.LoadPercentage}%")
```

## Miners

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_active_miners()` | `/activeminers` | `list[ActiveMiner]` | Currently active miners |
| `get_running_miners()` | `/runningminers` | `list[RunningMiner]` | Currently running miners |
| `get_failed_miners()` | `/failedminers` | `list[FailedMiner]` | Miners that have failed |
| `get_remote_miners(mode=)` | `/remoteminers` | `list[RemoteMiner] \| list[RemoteMinerEntry]` | Remote miners; `mode` changes shape |
| `get_miners_needing_benchmark()` | `/minersneedingbenchmark` | `list[Any]` | Miners needing re-benchmark |
| `get_miner_info()` | `/minerinfo` | `list[MinerInfo]` | Detailed miner info |
| `get_miner_speeds()` | `/minerspeeds` | `list[MinerSpeed]` | Speed per miner |
| `get_miners()` | `/miners` | `list[Miner]` | All miners |
| `get_fastest_miners()` | `/fastestminers` | `list[FastestMiner]` | Fastest miner per algorithm |
| `get_avail_miners()` | `/availminers` | `list[str]` | Available miner names |
| `get_avail_miner_stats()` | `/availminerstats` | `list[AvailMinerStat]` | Stats for available miners |
| `get_disabled()` | `/disabled` | `list[str]` | Disabled miner names |
| `get_miner_log(logfile=)` | `/getminerlog` | `MinerLogResult` | Miner log contents |
| `get_miner_stats()` | `/minerstats` | `list[MinerStat]` | Per-miner statistics |

### Example: Active miners

```python
from rainbowminer_api_client import RainbowMinerClient


async with RainbowMinerClient("192.168.1.50", 4000) as client:
    miners = await client.get_active_miners()
    for m in miners:
        print(f"{m.Name} ({m.Algorithm}): {m.Speed} {m.SpeedUnit}")
```

## Pools & algorithms

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_algorithms()` | `/algorithms` | `list[str]` | Supported algorithm names |
| `get_pools()` | `/pools` | `list[Pool]` | Active pools |
| `get_all_pools()` | `/allpools` | `list[AllPool]` | All known pools |
| `get_new_pools()` | `/newpools` | `list[NewPool]` | Pools available to add |

## Balances & earnings

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_balances(...)` | `/balances` | `list[Balance] \| BinaryResponse` | Pool balances |
| `get_payouts()` | `/payouts` | `list[Payout]` | Payout history |
| `get_earnings(...)` | `/earnings` | `EarningsResult` | Earnings report |
| `get_rates(format=)` | `/rates` | `dict[str, float] \| list[RateTableRow]` | Exchange rates |

!!! tip "CSV vs structured"

    `get_balances()`, `get_earnings()`, and `get_rates()` support optional
    parameters to control the response format. See the
    [binary endpoints](binary.md) for CSV download helpers.

## Devices

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_all_devices()` | `/alldevices` | `list[AllDevice]` | All devices |
| `get_devices()` | `/devices` | `list[Device]` | Active devices |
| `get_platforms()` | `/platforms` | `dict[str, Any]` | Platform info |
| `get_device_combos()` | `/devicecombos` | `list[DeviceCombo]` | Device combinations |
| `get_device_config()` | `/getdeviceconfig` | `list[DeviceConfigEntry]` | Device config entries |
| `get_oc_profiles()` | `/ocprofiles` | `list[OCProfile]` | Overclock profiles |

## Stats & totals

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_stats()` | `/stats` | `dict[str, Any]` | General stats |
| `get_totals()` | `/totals` | `list[Total]` | Totals per algorithm/coin |
| `get_activity(as_csv=)` | `/activity` | `list[Any] \| BinaryResponse` | Activity log |

## Config

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_config()` | `/config` | `Config` | Full server config |
| `get_user_config()` | `/userconfig` | `UserConfig` | User config |
| `get_setup()` | `/setup.json` | `SetupJson` | Setup info |

## MRR (MiningRigRentals)

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `get_mrr_stats()` | `/mrrstats` | `list[MrrStat]` | MRR stats |
| `get_mrr_rigs()` | `/mrrrigs` | `list[MrrRig]` | MRR rigs |
| `get_mrr_control()` | `/mrrcontrol` | `list[MrrControl]` | MRR control status |

## Misc

| Method | Endpoint | Returns | Description |
| ------ | -------- | ------- | ----------- |
| `load_config(config_name=, pool_name=)` | `/loadconfig` | `Any` | Load a config |
| `load_config_json(config_name=)` | `/loadconfigjson` | `LoadConfigJsonResult` | Load config as JSON |
| `get_wtm_urls()` | `/getwtmurls` | `dict[str, str]` | WhatToMine URLs |
| `get_session_vars()` | `/sessionvars` | `dict[str, Any]` | Session variables |
| `get_session()` | `/session` | `dict[str, Any]` | Session info |
| `get_gc()` | `/gc` | `dict[str, Any]` | Garbage collection stats |
| `get_watchdog_timers()` | `/watchdogtimers` | `list[Any]` | Watchdog timers |
| `get_crash_counter()` | `/crashcounter` | `list[Any]` | Crash counter |
| `get_asyncloader_jobs()` | `/asyncloaderjobs` | `list[AsyncloaderJob]` | Async loader jobs |
| `get_dec_sep()` | `/decsep` | `str` | Decimal separator |
| `get_clients(include_server=)` | `/clients` | `list[Client]` | Connected clients |
| `get_download_list()` | `/downloadlist` | `list[DownloadItem]` | Available downloads |

## Next steps

- [:octicons-arrow-right-24: Control endpoints](control.md) — pause, reboot, toggle
- [:octicons-arrow-right-24: API reference](../reference/client.md) — full method docs
