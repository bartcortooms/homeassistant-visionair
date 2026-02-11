"""Data coordinator for VisionAir devices."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from bleak import BleakClient
from bleak.exc import BleakError
from .visionair_ble import VisionAirClient, DeviceStatus

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DOMAIN

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice

_LOGGER = logging.getLogger(__name__)


class VisionAirCoordinator(DataUpdateCoordinator[DeviceStatus]):
    """Coordinator for VisionAir device data."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        update_interval: int = DEFAULT_UPDATE_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"VisionAir {address}",
            update_interval=timedelta(seconds=update_interval),
        )
        self.address = address
        self._client: VisionAirClient | None = None

    async def _async_update_data(self) -> DeviceStatus:
        """Fetch data from the device.

        Uses get_fresh_status() which sends three BLE requests to collect
        fresh temperature and humidity readings for all probes and the remote.
        """
        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, self.address, connectable=True
        )
        if not ble_device:
            raise UpdateFailed(f"Device {self.address} not found")

        try:
            async with BleakClient(ble_device) as client:
                visionair = VisionAirClient(client)
                status = await visionair.get_fresh_status()

                _LOGGER.debug(
                    "VisionAir status update - temp_remote: %s, temp_probe1: %s, "
                    "temp_probe2: %s, humidity: %s, filter_days: %s, airflow_mode: %s",
                    status.temp_remote,
                    status.temp_probe1,
                    status.temp_probe2,
                    status.humidity_remote,
                    status.filter_days,
                    status.airflow_mode,
                )
                return status
        except BleakError as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err
        except TimeoutError as err:
            raise UpdateFailed(f"Timeout communicating with device: {err}") from err

    async def _async_send_command(self, action: str, command) -> None:
        """Send a command to the device and update coordinator data."""
        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, self.address, connectable=True
        )
        if not ble_device:
            raise HomeAssistantError(f"Device {self.address} not found")

        try:
            async with BleakClient(ble_device) as client:
                visionair = VisionAirClient(client)
                new_status = await command(visionair)
                self.async_set_updated_data(new_status)
        except (BleakError, TimeoutError) as err:
            raise HomeAssistantError(f"Error {action}: {err}") from err

    async def async_set_airflow_mode(self, mode: str) -> None:
        """Set the airflow mode."""
        await self._async_send_command(
            "setting airflow mode", lambda v: v.set_airflow_mode(mode)
        )

    async def async_set_boost(self, enable: bool) -> None:
        """Enable or disable boost mode."""
        await self._async_send_command(
            "setting boost", lambda v: v.set_boost(enable)
        )

    async def async_set_preheat(self, enabled: bool) -> None:
        """Set preheat on/off."""
        await self._async_send_command(
            "setting preheat", lambda v: v.set_preheat(enabled)
        )

    async def async_set_holiday(self, days: int) -> None:
        """Set holiday mode duration (0 to disable)."""
        await self._async_send_command(
            "setting holiday mode", lambda v: v.set_holiday(days)
        )

    async def async_set_preheat_temperature(self, temperature: int) -> None:
        """Set preheat temperature (14-22°C)."""
        await self._async_send_command(
            "setting preheat temperature", lambda v: v.set_preheat_temperature(temperature)
        )

    async def async_set_summer_limit(self, enabled: bool) -> None:
        """Set summer limit."""
        await self._async_send_command(
            "setting summer limit", lambda v: v.set_summer_limit(enabled)
        )
