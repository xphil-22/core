"""Module to define the CrealityLight class for controlling Creality printers as lights."""

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Creality light platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([CrealityLight(coordinator)])


class CrealityLight(CoordinatorEntity, LightEntity):
    """Representation of a Creality printer as a light entity."""

    def __init__(self, coordinator: CrealityDataUpdateCoordinator) -> None:
        """Initialize the CrealityLight entity.

        :param coordinator: The data coordinator.
        """
        super().__init__(coordinator)
        self._name = "Creality K1 Light"
        self._state = False

    @property
    def name(self):
        """Return the name of the light."""
        return self._name

    @property
    def is_on(self):
        """Return the current state of the light."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        self._state = False
        self.async_write_ha_state()

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
        if "lightSw" in self.coordinator.data:
            if isinstance(bool, self.coordinator.data["lightSw"]):
                self._state = self.coordinator.data["lightSw"]
                self.async_write_ha_state()
