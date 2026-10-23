"""Config flow for Tapo Direct."""
from __future__ import annotations
from typing import Any
from kasa import Credentials, Device, DeviceConfig, KasaException
from kasa.deviceconfig import DeviceConnectionParameters, DeviceEncryptionType, DeviceFamily
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN
def _device_config(data: dict[str, Any]) -> DeviceConfig:
    return DeviceConfig(host=data[CONF_HOST], credentials=Credentials(data[CONF_USERNAME], data[CONF_PASSWORD]), connection_type=DeviceConnectionParameters(DeviceFamily.SmartTapoBulb, DeviceEncryptionType.Klap, login_version=2, https=False, http_port=80), timeout=10)
class TapoDirectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})
            device = None
            try:
                device = await Device.connect(config=_device_config(user_input))
                await self.async_set_unique_id(device.device_id)
                self._abort_if_unique_id_configured(updates={CONF_HOST: user_input[CONF_HOST]})
                return self.async_create_entry(title=device.alias or f"Tapo {device.model}", data=user_input)
            except KasaException:
                errors["base"] = "cannot_connect"
            finally:
                if device is not None:
                    await device.protocol.close()
        return self.async_show_form(step_id="user", data_schema=vol.Schema({vol.Required(CONF_HOST): str, vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}), errors=errors)
