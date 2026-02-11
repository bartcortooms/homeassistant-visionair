"""Switch platform for VisionAir integration."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from .visionair_ble import DeviceStatus

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VisionAirCoordinator


@dataclass(frozen=True, kw_only=True)
class VisionAirSwitchEntityDescription(SwitchEntityDescription):
    """Describes a VisionAir switch entity."""

    value_fn: Callable[[DeviceStatus], bool]
    turn_on_fn: Callable[[VisionAirCoordinator], Coroutine[Any, Any, None]]
    turn_off_fn: Callable[[VisionAirCoordinator], Coroutine[Any, Any, None]]


SWITCH_DESCRIPTIONS: tuple[VisionAirSwitchEntityDescription, ...] = (
    VisionAirSwitchEntityDescription(
        key="preheat",
        translation_key="preheat",
        value_fn=lambda data: data.preheat_enabled,
        turn_on_fn=lambda coord: coord.async_set_preheat(True),
        turn_off_fn=lambda coord: coord.async_set_preheat(False),
    ),
    VisionAirSwitchEntityDescription(
        key="summer_limit",
        translation_key="summer_limit",
        value_fn=lambda data: data.summer_limit_enabled,
        turn_on_fn=lambda coord: coord.async_set_summer_limit(True),
        turn_off_fn=lambda coord: coord.async_set_summer_limit(False),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VisionAir switches from a config entry."""
    coordinator: VisionAirCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        VisionAirSwitch(coordinator, entry, description)
        for description in SWITCH_DESCRIPTIONS
    )


class VisionAirSwitch(CoordinatorEntity[VisionAirCoordinator], SwitchEntity):
    """Representation of a VisionAir switch."""

    _attr_has_entity_name = True
    entity_description: VisionAirSwitchEntityDescription

    def __init__(
        self,
        coordinator: VisionAirCoordinator,
        entry: ConfigEntry,
        description: VisionAirSwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.data['address']}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": entry.title,
            "manufacturer": "Ventilairsec",
            "model": "VisionAir",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if the switch is on."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        await self.entity_description.turn_on_fn(self.coordinator)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        await self.entity_description.turn_off_fn(self.coordinator)
