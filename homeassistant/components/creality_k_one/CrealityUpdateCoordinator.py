"""Module to define the CrealityDataUpdateCoordinator class for managing data updates from Creality printers."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .CrealityApi import CrealityApi

_LOGGER = logging.getLogger(__name__)


class CrealityDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator for managing data updates from Creality printers."""

    def __init__(self, hass: HomeAssistant, api: CrealityApi) -> None:
        """Initialize the coordinator.

        :param hass: The Home Assistant instance.
        :param api: The CrealityApi instance.
        """
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name="Creality K1",
        )
        self.api.register_callback(self._handle_update)

    async def _handle_update(self, data):
        """Handle update from WebSocket.

        :param data: The updated data.
        """
        self.async_set_updated_data(data)

    async def async_close(self):
        """Close the API connection."""
        await self.api.close()
