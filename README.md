# Tapo Direct

Experimental Home Assistant custom integration for Tapo bulbs that are reachable through KLAP v2 but cannot be configured by normal discovery.

The integration uses a fixed local connection profile:

- device family: SMART.TAPOBULB
- encryption: KLAP v2
- transport: HTTP port 80
- no cloud control and no discovery

It was developed and tested with a TP-Link Tapo L530 on Home Assistant 2026.10.2.

## Installation with HACS

1. Open HACS.
2. Add this repository as a custom repository in category **Integration**.
3. Download **Tapo Direct**.
4. Restart Home Assistant.
5. Open **Settings → Devices & services → Add integration → Tapo Direct**.
6. Enter the bulb IP address and TP-Link account credentials.

## Coexistence

The integration uses the unique domain `tapo_direct` and does not override Home Assistant's built-in `tplink` integration. Do not configure the same bulb in multiple controllers at once: concurrent KLAP sessions can invalidate each other.

## Supported features

- local state polling
- on/off
- brightness
- color temperature
- hue and saturation

## Status and scope

This is an early release for devices matching the connection profile above. Other Tapo models and firmware variants may use different transports and are not assumed to be compatible.

## Rollback

Remove the Tapo Direct config entry, uninstall the repository through HACS and restart Home Assistant if requested. The built-in TP-Link integration is never replaced.

## License

MIT
