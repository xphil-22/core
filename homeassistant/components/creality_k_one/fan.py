"""Module to define the CrealityLight class for controlling Creality printers as lights."""

import logging
from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.percentage import (
    int_states_in_range,
    percentage_to_ranged_value,
)

from .const import DOMAIN, FANS
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator

logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Creality light platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([CrealityFan(coordinator, fan) for fan in FANS])


SPEED_RANGE = (1, 255)
PRESET_MODES = ["low", "middle", "high", "full"]
PRESET_PERCENTAGES = {"low": 25, "middle": 50, "high": 75, "full": 100}


class CrealityFan(CoordinatorEntity, FanEntity):
    """Representation of a Creality printer fan."""

    def __init__(self, coordinator: CrealityDataUpdateCoordinator, fan) -> None:
        """Initialize the CrealityFan entity."""
        super().__init__(coordinator)
        self._attr_unique_id = fan["id"]
        self._name = fan["friendly_name"]
        self._is_on: None | bool = None
        self._attr_percentage = None
        self._percentage_get = fan["percentage_get_command"]
        self.fan_number: int = fan["fan_number"]
        self._speed_change_command = f"M106 P{fan['fan_number']} S{{}}"
        self._attr_supported_features = (
            FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE
        )
        self._attr_preset_modes = PRESET_MODES

    @property
    def name(self) -> str:
        """Return the name of the fan."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if the fan is on."""
        return self._is_on

    @property
    def percentage(self) -> int | None:
        """Return the current speed percentage."""
        return self._attr_percentage

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return int_states_in_range(SPEED_RANGE)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the fan."""
        self._is_on = True
        await self.coordinator.api.send_message(
            {"method": "set", "params": {self._attr_unique_id: 1}}
        )
        self.async_write_ha_state()

    async def async_turn_off(self, **kwags: Any) -> None:
        """Turn off the fan."""
        self._is_on = False
        await self.coordinator.api.send_message(
            {"method": "set", "params": {self._attr_unique_id: 0}}
        )
        self.async_write_ha_state()

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        self.hass.async_add_executor_job(self.async_set_percentage, percentage)

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        if percentage == 0:
            self._is_on = False
            self.async_write_ha_state()
        elif not self._is_on:
            self._is_on = True
            self.async_write_ha_state()

        self._attr_percentage = percentage
        value_in_range = int(percentage_to_ranged_value(SPEED_RANGE, percentage))
        argument = f"M106 P{str(self.fan_number)} S{str(value_in_range)}"
        msg = {
            "method": "set",
            "params": {"gcodeCmd": argument},
        }
        await self.coordinator.api.send_message(msg)
        self.async_write_ha_state()

    def _handle_update(self, data):
        if self._attr_unique_id in data:
            self._is_on = data[self._attr_unique_id] == 1
        if self._percentage_get in data:
            self._attr_percentage = data[self._percentage_get]
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._handle_update(self.coordinator.data)

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        if preset_mode not in PRESET_MODES:
            raise ValueError(f"Invalid preset mode: {preset_mode}")
        self.set_percentage(PRESET_PERCENTAGES[preset_mode])
        logger.info(
            "Fan preset mode set to: %s (%s%%)", preset_mode, self._attr_percentage
        )

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        await self.hass.async_add_executor_job(self.set_preset_mode, preset_mode)

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        initial_data = self.coordinator.api.get_initial_data()
        if initial_data:
            self._handle_update(initial_data)
