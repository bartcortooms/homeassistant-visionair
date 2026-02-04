"""Sensor platform for VisionAir integration.

Sensors are auto-generated from field metadata in DeviceStatus.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from .visionair_ble import DeviceStatus

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VisionAirCoordinator


# Map library units to HA units
UNIT_MAP = {
    "°C": UnitOfTemperature.CELSIUS,
    "%": PERCENTAGE,
    "d": UnitOfTime.DAYS,
    "m³/h": "m³/h",  # HA doesn't have a constant for this
    "m³": "m³",
}

# Map library device_class to HA SensorDeviceClass
DEVICE_CLASS_MAP = {
    "temperature": SensorDeviceClass.TEMPERATURE,
    "humidity": SensorDeviceClass.HUMIDITY,
    "duration": SensorDeviceClass.DURATION,
    "volume_flow_rate": SensorDeviceClass.VOLUME_FLOW_RATE,
    "enum": SensorDeviceClass.ENUM,
}

# Map library state_class to HA SensorStateClass
STATE_CLASS_MAP = {
    "measurement": SensorStateClass.MEASUREMENT,
    "total_increasing": SensorStateClass.TOTAL_INCREASING,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VisionAir sensors from a config entry."""
    coordinator: VisionAirCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for field_info in dataclasses.fields(DeviceStatus):
        meta = field_info.metadata
        if not meta.get("sensor"):
            continue

        entities.append(VisionAirSensor(
            coordinator=coordinator,
            entry=entry,
            field_name=field_info.name,
            name=meta.get("name", field_info.name),
            unit=UNIT_MAP.get(meta.get("unit"), meta.get("unit")),
            device_class=DEVICE_CLASS_MAP.get(meta.get("device_class")),
            state_class=STATE_CLASS_MAP.get(meta.get("state_class")),
            enabled_default=meta.get("enabled_default", True),
            options=meta.get("options"),
            precision=meta.get("precision"),
        ))

    async_add_entities(entities)


class VisionAirSensor(CoordinatorEntity[VisionAirCoordinator], SensorEntity):
    """Representation of a VisionAir sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: VisionAirCoordinator,
        entry: ConfigEntry,
        field_name: str,
        name: str,
        unit: str | None,
        device_class: SensorDeviceClass | None,
        state_class: SensorStateClass | None,
        enabled_default: bool,
        options: list[str] | None,
        precision: int | None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._field_name = field_name
        self._attr_name = name  # Use name from library metadata
        self._attr_unique_id = f"{entry.data['address']}_{field_name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_entity_registry_enabled_default = enabled_default
        self._attr_options = options
        self._attr_suggested_display_precision = precision
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["address"])},
            "name": entry.title,
            "manufacturer": "Ventilairsec",
            "model": "VisionAir",
        }

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return getattr(self.coordinator.data, self._field_name, None)
