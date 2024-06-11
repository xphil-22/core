"""Module to define the CrealityLight class for controlling Creality printers as lights."""

import logging

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LIGHTS
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator

logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Creality light platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            CrealityLight(coordinator, light["id"], light["friendly_name"])
            for light in LIGHTS
        ]
    )


class CrealityLight(CoordinatorEntity, LightEntity):
    """Representation of a Creality printer as a light entity."""

    def __init__(
        self,
        coordinator: CrealityDataUpdateCoordinator,
        light_id: str,
        friendly_name: str,
    ) -> None:
        """Initialize the CrealityLight entity.

        :param coordinator: The data coordinator.
        """
        super().__init__(coordinator)
        self._attr_unique_id = light_id
        self._name = friendly_name
        self._state = False

    @property
    def name(self):
        """Return the name of the light."""
        return self._name

    @property
    def is_on(self):
        """Return the current state of the light."""
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
        logger.error("handle coordinator update with: ")
        logger.error(self.coordinator.data)
        if self._attr_unique_id in self.coordinator.data:
            logger.error("check if bool")
            logger.error(self.coordinator.data[self._attr_unique_id])
            if isinstance(self.coordinator.data[self._attr_unique_id], int):
                logger.error("set new state")
                self._state = self.coordinator.data[self._attr_unique_id] == 1
                self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn on the light."""
        self._state = True
        await self.coordinator.api.send_message(
            {"method": "set", "params": {self._attr_unique_id: 1}}
        )
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        self._state = False
        await self.coordinator.api.send_message(
            {"method": "set", "params": {self._attr_unique_id: 0}}
        )
        self.async_write_ha_state()
