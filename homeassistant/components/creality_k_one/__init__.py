"""The Creality K1 integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .CrealityApi import CrealityApi
from .CrealityUpdateCoordinator import CrealityDataUpdateCoordinator

# List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.LIGHT]


# philipp admin123
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Creality K1 from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    uri = f"ws://{entry.data['host']}:{entry.data['port']}"
    uri = "ws://100.122.222.209:9999"
    # 1. Create API instance
    api = CrealityApi(uri)
    try:
        await api.connect()
    except Exception as e:
        api.close()
        raise e

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
