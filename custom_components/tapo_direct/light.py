"""Light platform for Tapo Direct."""
from __future__ import annotations
from typing import Any
from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_COLOR_TEMP_KELVIN, ATTR_HS_COLOR, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import TapoDirectCoordinator
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    async_add_entities([TapoDirectLight(entry.runtime_data)])
class TapoDirectLight(CoordinatorEntity[TapoDirectCoordinator], LightEntity):
    _attr_has_entity_name = True
    _attr_name = None
    def __init__(self, coordinator: TapoDirectCoordinator) -> None:
        super().__init__(coordinator)
        device = coordinator.device
        self._attr_unique_id = device.device_id
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, device.device_id)}, name=device.alias or device.model, manufacturer="TP-Link", model=device.model)
    @property
    def is_on(self) -> bool:
        return self.coordinator.device.is_on
    @property
    def brightness(self) -> int | None:
        value = getattr(self.coordinator.device, "brightness", None)
        return round(value * 255 / 100) if value is not None else None
    @property
    def hs_color(self) -> tuple[float, float] | None:
        hsv = getattr(self.coordinator.device, "hsv", None)
        return (float(hsv.hue), float(hsv.saturation)) if hsv else None
    @property
    def color_temp_kelvin(self) -> int | None:
        return getattr(self.coordinator.device, "color_temp", None)
    @property
    def supported_color_modes(self) -> set[ColorMode]:
        return {ColorMode.COLOR_TEMP, ColorMode.HS}

    @property
    def color_mode(self) -> ColorMode:
        """Return the currently active color mode."""
        color_temp = getattr(self.coordinator.device, "color_temp", None)
        return ColorMode.COLOR_TEMP if color_temp else ColorMode.HS
    async def async_turn_on(self, **kwargs: Any) -> None:
        device = self.coordinator.device
        if ATTR_HS_COLOR in kwargs:
            hue, saturation = kwargs[ATTR_HS_COLOR]
            brightness = round(kwargs.get(ATTR_BRIGHTNESS, 255) * 100 / 255)
            await device.set_hsv(round(hue), round(saturation), brightness)
        elif ATTR_COLOR_TEMP_KELVIN in kwargs:
            await device.set_color_temp(kwargs[ATTR_COLOR_TEMP_KELVIN])
            if ATTR_BRIGHTNESS in kwargs:
                await device.set_brightness(round(kwargs[ATTR_BRIGHTNESS] * 100 / 255))
        elif ATTR_BRIGHTNESS in kwargs:
            await device.set_brightness(round(kwargs[ATTR_BRIGHTNESS] * 100 / 255))
        else:
            await device.turn_on()
        await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.device.turn_off()
        await self.coordinator.async_request_refresh()
