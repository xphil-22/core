"""Module to define the CrealityLight class for controlling Creality printers as lights."""

import logging

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import BUTTONS, DOMAIN
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
            CrealityButton(
                coordinator,
                button["id"],
                button["friendly_name"],
                ButtonDeviceClass.RESTART,
            )
            for button in BUTTONS
        ]
    )


class CrealityButton(CoordinatorEntity, ButtonEntity):
    """Represents a button of the Creality K1."""

    def __init__(
        self,
        coordinator: CrealityDataUpdateCoordinator,
        button_id: str,
        button_name: str,
        device_class: ButtonDeviceClass | None,
    ) -> None:
        """Initialize the CrealityLight entity.

        :param coordinator: The data coordinator.
        """
        super().__init__(coordinator)
        self._attr_unique_id = button_id
        self._name = button_name
        self._attr_device_class = device_class

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.api.send_message(
            {"method": "set", "params": {"restartKlipper": 1}}
        )
        await self.coordinator.api.send_message(
            {"method": "set", "params": {"restartFirmware": 1}}
        )
        self.async_write_ha_state()
