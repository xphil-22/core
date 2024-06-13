"""The Creality K1 integration."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .CrealityApi import CrealityApi
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator

# {"method":"set","params":{"restartKlipper":1}}
#
# List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.FAN,
    Platform.BUTTON,
    # Platform.CAMERA,
]


# philipp admin123
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Creality K1 from a config entry."""
    logging.error("try to set up creality k1..")
    hass.data.setdefault(DOMAIN, {})
    uri = f"ws://{entry.data['host']}:{entry.data['port']}"
    # uri = "ws://100.122.222.170:8765"
    uri = "ws://100.122.222.209:9999"
    # 1. Create API instance
    api = CrealityApi(uri)
    try:
        await api.connect()
    except asyncio.TimeoutError as e:
        raise ConfigEntryNotReady("Timeout while connecting..") from e

    # 2. Create the DataUpdateCoordinator
    coordinator = CrealityDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    # 3. Store the coordinator for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    await coordinator.api.close()
    return ok
