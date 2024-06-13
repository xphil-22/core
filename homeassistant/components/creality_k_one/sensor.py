"""Module to define the CrealitySensor class for monitoring Creality printers."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSORS
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator

logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Creality sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            CrealitySensor(coordinator, sensor["id"], sensor["friendly_name"])
            for sensor in SENSORS
        ]
    )


class CrealitySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Creality printer sensor."""

    def __init__(
        self,
        coordinator: CrealityDataUpdateCoordinator,
        sensor_id: str,
        friendly_name: str,
    ) -> None:
        """Initialize the CrealitySensor entity.

        :param coordinator: The data coordinator.
        :param sensor_id: ID of the sensor.
        :param friendly_name: Friendly name of the sensor.
        """
        super().__init__(coordinator)
        self._attr_unique_id = sensor_id
        self._name = friendly_name
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the current state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        return self.coordinator.data

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self):
        """Run when entity about to be removed from hass."""
        await super().async_will_remove_from_hass()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._attr_unique_id in self.coordinator.data:
            self._state = self.coordinator.data[self._attr_unique_id]
            self.async_write_ha_state()
