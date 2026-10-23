# Tapo Direct

Experimental Home Assistant custom integration for a Tapo bulb whose normal discovery reports an unusable protocol. It connects directly with SMART.TAPOBULB, KLAP v2 and HTTP port 80.

## Status
Development prototype. Do not install until the read-only connection and entity behavior have been validated.

## Safety
- Domain: tapo_direct; it does not replace Home Assistant's tplink domain.
- Configure a device in only one integration to avoid duplicate entities and competing polling/control.
- Credentials are stored in the Home Assistant config entry.

## Rollback
Remove the Tapo Direct config entry, uninstall the custom repository and restart Home Assistant if required. The built-in TP-Link integration is not modified.
