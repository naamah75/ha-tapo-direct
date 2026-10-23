"""Tapo Direct integration."""
from __future__ import annotations
from datetime import timedelta
from kasa import Credentials, Device, DeviceConfig, KasaException
from kasa.deviceconfig import DeviceConnectionParameters, DeviceEncryptionType, DeviceFamily
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, PLATFORMS
from .coordinator import TapoDirectCoordinator
type TapoDirectConfigEntry = ConfigEntry[TapoDirectCoordinator]
def build_device_config(entry: ConfigEntry) -> DeviceConfig:
    """Build the known-working direct KLAP v2 configuration."""
    return DeviceConfig(host=entry.data[CONF_HOST], credentials=Credentials(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD]), connection_type=DeviceConnectionParameters(device_family=DeviceFamily.SmartTapoBulb, encryption_type=DeviceEncryptionType.Klap, login_version=2, https=False, http_port=80), timeout=10)
async def async_setup_entry(hass: HomeAssistant, entry: TapoDirectConfigEntry) -> bool:
    try:
        device = await Device.connect(config=build_device_config(entry))
    except KasaException as err:
        raise ConfigEntryNotReady(str(err)) from err
    coordinator = TapoDirectCoordinator(hass, entry, device, timedelta(seconds=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)))
    entry.runtime_data = coordinator
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
async def async_unload_entry(hass: HomeAssistant, entry: TapoDirectConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.device.protocol.close()
    return unloaded
