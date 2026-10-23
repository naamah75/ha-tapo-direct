"""Data coordinator for Tapo Direct."""
from __future__ import annotations
from datetime import timedelta
import logging
from kasa import AuthenticationError, Device, KasaException
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
_LOGGER = logging.getLogger(__name__)
class TapoDirectCoordinator(DataUpdateCoordinator[None]):
    """Poll one directly configured Tapo light."""
    config_entry: ConfigEntry
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, device: Device, update_interval: timedelta) -> None:
        super().__init__(hass, _LOGGER, name=f"tapo_direct-{device.host}", config_entry=entry, update_interval=update_interval)
        self.device = device
    async def _async_update_data(self) -> None:
        try:
            await self.device.update()
        except AuthenticationError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except KasaException as err:
            raise UpdateFailed(str(err)) from err
