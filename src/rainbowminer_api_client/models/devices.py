"""Models for device-related endpoints.

Covers: ``/alldevices``, ``/devices``, ``/devicecombos``, ``/getdeviceconfig``,
``/ocprofiles``, ``/cpuinfo``, ``/sysinfo``.
"""

from __future__ import annotations

from typing import Any

from rainbowminer_api_client.models._base import RainbowMinerModel

__all__ = [
    "AllDevice",
    "Device",
    "DeviceCombo",
    "DeviceConfigEntry",
    "OCProfile",
]


class AllDevice(RainbowMinerModel):
    """An entry from ``/alldevices`` — a hardware device detected by RainbowMiner.

    Attributes:
        Type: Device type (``"Gpu"`` or ``"Cpu"``).
        Vendor: Vendor name (``"NVIDIA"``, ``"AMD"``, ``"INTEL"``).
        Model: Device model name.
        Name: Display name.
        Data: Vendor-specific device data.
    """

    Type: str | None = None
    Vendor: str | None = None
    Model: str | None = None
    Name: str | None = None
    Data: dict[str, Any] | None = None


class Device(RainbowMinerModel):
    """An entry from ``/devices`` — selected/enabled devices.

    Attributes:
        Type: Device type (``"Gpu"`` or ``"Cpu"``).
        Vendor: Vendor name (``"NVIDIA"``, ``"AMD"``, ``"INTEL"``).
        Model: Device model name.
        Name: Display name.
    """

    Type: str | None = None
    Vendor: str | None = None
    Model: str | None = None
    Name: str | None = None


class DeviceCombo(RainbowMinerModel):
    """An entry from ``/devicecombos``.

    Newer servers return a plain list of device-name strings (e.g.
    ``["CPU", "GPU#0"]``); this model is kept for forward-compatibility if
    the server ever returns structured objects.
    """

    Name: str | None = None


class DeviceConfigEntry(RainbowMinerModel):
    """An entry from ``/getdeviceconfig``.

    Attributes:
        Name: Device or vendor name.
        Selected: Whether the device is selected for mining.
        Excluded: Whether the device is explicitly excluded.
        Cores: CPU core count (CPU entries only).
        Threads: CPU thread count (CPU entries only).
    """

    Name: str = ""
    Selected: bool = False
    Excluded: bool = False
    Cores: int | None = None
    Threads: int | None = None


class OCProfile(RainbowMinerModel):
    """An entry from ``/ocprofiles`` — an overclock profile.

    Attributes:
        Name: Profile name.
        Device: Target device label.
        PowerLimit: Power limit percentage.
        ThermalLimit: Thermal limit in degrees Celsius.
        MemoryClockBoost: Memory clock offset in MHz.
        CoreClockBoost: Core clock offset in MHz.
        LockVoltagePoint: Locked voltage point in mV.
        LockMemoryClock: Locked memory clock in MHz.
        LockCoreClock: Locked core clock in MHz.
    """

    Name: str = ""
    Device: str = ""
    PowerLimit: float | int | str | None = None
    ThermalLimit: float | int | str | None = None
    MemoryClockBoost: float | int | str | None = None
    CoreClockBoost: float | int | str | None = None
    LockVoltagePoint: float | int | str | None = None
    LockMemoryClock: float | int | str | None = None
    LockCoreClock: float | int | str | None = None
