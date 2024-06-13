"""Represents Binary Sensors."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import BINARY_SENSORS, DOMAIN
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Creality light platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            CrealityBinarySensor(
                coordinator,
                button["id"],
                button["friendly_name"],
            )
            for button in BINARY_SENSORS
        ]
    )


class CrealityBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Creality printer binary sensor."""

    def __init__(
        self,
        coordinator: CrealityDataUpdateCoordinator,
        sensor_id: str,
        friendly_name: str,
    ) -> None:
        """Initialize the CrealityBinarySensor entity."""
        super().__init__(coordinator)
        self._attr_unique_id = sensor_id
        self._name = friendly_name
        self._state = False  # Default state for a binary sensor

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._name

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._state

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._attr_unique_id in self.coordinator.data:
            # Adjust this logic based on your actual data
            self._state = self.coordinator.data[self._attr_unique_id] == 1
            self.async_write_ha_state()
