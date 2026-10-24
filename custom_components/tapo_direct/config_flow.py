"""Config flow for Tapo Direct."""
from __future__ import annotations

from typing import Any, Mapping

from kasa import AuthenticationError, Credentials, Device, DeviceConfig, KasaException
from kasa.deviceconfig import (
    DeviceConnectionParameters,
    DeviceEncryptionType,
    DeviceFamily,
)
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


def _device_config(data: Mapping[str, Any]) -> DeviceConfig:
    """Build the fixed KLAP v2 connection configuration."""
    return DeviceConfig(
        host=data[CONF_HOST],
        credentials=Credentials(data[CONF_USERNAME], data[CONF_PASSWORD]),
        connection_type=DeviceConnectionParameters(
            DeviceFamily.SmartTapoBulb,
            DeviceEncryptionType.Klap,
            login_version=2,
            https=False,
            http_port=80,
        ),
        timeout=10,
    )


async def _async_validate_connection(data: Mapping[str, Any]) -> Device:
    """Connect to the bulb and return the initialized device."""
    return await Device.connect(config=_device_config(data))


class TapoDirectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tapo Direct."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})
            device = None
            try:
                device = await _async_validate_connection(user_input)
                await self.async_set_unique_id(device.device_id)
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: user_input[CONF_HOST]}
                )
                return self.async_create_entry(
                    title=device.alias or f"Tapo {device.model}", data=user_input
                )
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except KasaException:
                errors["base"] = "cannot_connect"
            finally:
                if device is not None:
                    await device.protocol.close()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> FlowResult:
        """Start reauthentication after an authentication failure."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Validate replacement credentials and update the config entry."""
        reauth_entry = self._get_reauth_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            updated_data = {
                **reauth_entry.data,
                CONF_USERNAME: user_input[CONF_USERNAME],
                CONF_PASSWORD: user_input[CONF_PASSWORD],
            }
            device = None
            try:
                device = await _async_validate_connection(updated_data)
                await self.async_set_unique_id(device.device_id)
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(
                    reauth_entry,
                    data_updates=updated_data,
                )
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except KasaException:
                errors["base"] = "cannot_connect"
            finally:
                if device is not None:
                    await device.protocol.close()

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=reauth_entry.data[CONF_USERNAME],
                    ): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
