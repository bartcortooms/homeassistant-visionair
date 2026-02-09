"""Number platform for VisionAir integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VisionAirCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VisionAir number entities from a config entry."""
    coordinator: VisionAirCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        VisionAirHolidayDays(coordinator, entry),
        VisionAirPreheatTemperature(coordinator, entry),
    ])


class VisionAirHolidayDays(CoordinatorEntity[VisionAirCoordinator], NumberEntity):
    """Number entity for setting holiday mode duration."""

    _attr_has_entity_name = True
    _attr_translation_key = "holiday_days"
    _attr_native_min_value = 0
    _attr_native_max_value = 30
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTime.DAYS
    _attr_mode = NumberMode.BOX
    _attr_icon = "mdi:palm-tree"

    def __init__(
        self,
        coordinator: VisionAirCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['address']}_holiday_days"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": entry.title,
            "manufacturer": "Ventilairsec",
            "model": "VisionAir",
        }

    @property
    def native_value(self) -> float | None:
        """Return the current holiday days value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.holiday_days

    async def async_set_native_value(self, value: float) -> None:
        """Set holiday mode duration."""
        await self.coordinator.async_set_holiday(int(value))


class VisionAirPreheatTemperature(CoordinatorEntity[VisionAirCoordinator], NumberEntity):
    """Number entity for setting preheat temperature."""

    _attr_has_entity_name = True
    _attr_translation_key = "preheat_temperature"
    _attr_native_min_value = 12
    _attr_native_max_value = 18
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:thermometer"

    def __init__(
        self,
        coordinator: VisionAirCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['address']}_preheat_temperature"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": entry.title,
            "manufacturer": "Ventilairsec",
            "model": "VisionAir",
        }

    @property
    def native_value(self) -> float | None:
        """Return the current preheat temperature."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.preheat_temp

    async def async_set_native_value(self, value: float) -> None:
        """Set preheat temperature."""
        await self.coordinator.async_set_preheat_temperature(int(value))
