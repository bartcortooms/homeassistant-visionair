"""Fan platform for VisionAir integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.fan import (
    FanEntity,
    FanEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    PRESET_BOOST,
    PRESET_NONE,
    SPEED_HIGH,
    SPEED_LOW,
    SPEED_MEDIUM,
)
from .coordinator import VisionAirCoordinator

_LOGGER = logging.getLogger(__name__)

SPEED_LIST = [SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]
PRESET_MODES = [PRESET_NONE, PRESET_BOOST]

# Map speed names to percentage ranges
SPEED_TO_PERCENTAGE = {
    SPEED_LOW: 33,
    SPEED_MEDIUM: 66,
    SPEED_HIGH: 100,
}

PERCENTAGE_TO_SPEED = {
    (0, 33): SPEED_LOW,
    (34, 66): SPEED_MEDIUM,
    (67, 100): SPEED_HIGH,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VisionAir fan from a config entry."""
    coordinator: VisionAirCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VisionAirFan(coordinator, entry)])


class VisionAirFan(CoordinatorEntity[VisionAirCoordinator], FanEntity):
    """Representation of a VisionAir ventilation fan."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_translation_key = "visionair"
    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.PRESET_MODE
    )
    _attr_speed_count = 3
    _attr_preset_modes = PRESET_MODES

    def __init__(
        self,
        coordinator: VisionAirCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the fan."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data['address']}_fan"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": entry.title,
            "manufacturer": "Ventilairsec",
            "model": "VisionAir",
        }

    @property
    def is_on(self) -> bool:
        """Return true if the fan is on."""
        # Fan is always on for ventilation systems
        return True

    @property
    def percentage(self) -> int | None:
        """Return the current speed percentage."""
        if self.coordinator.data is None:
            return None

        mode = self.coordinator.data.airflow_mode
        return SPEED_TO_PERCENTAGE.get(mode, 66)

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        if self.coordinator.data is None:
            return None

        if self.coordinator.data.boost_active:
            return PRESET_BOOST
        return PRESET_NONE

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        if percentage == 0:
            # Can't turn off ventilation, set to low instead
            percentage = 33

        # Convert percentage to speed mode
        if percentage <= 33:
            mode = SPEED_LOW
        elif percentage <= 66:
            mode = SPEED_MEDIUM
        else:
            mode = SPEED_HIGH

        await self.coordinator.async_set_airflow_mode(mode)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        if preset_mode == PRESET_BOOST:
            await self.coordinator.async_set_boost(True)
        else:
            await self.coordinator.async_set_boost(False)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the fan."""
        if preset_mode is not None:
            await self.async_set_preset_mode(preset_mode)
        elif percentage is not None:
            await self.async_set_percentage(percentage)
        # If neither specified, fan is already on

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the fan (set to low - can't fully turn off ventilation)."""
        await self.coordinator.async_set_airflow_mode(SPEED_LOW)
