"""Constants for Tapo Direct."""
from datetime import timedelta
DOMAIN = "tapo_direct"
PLATFORMS = ["light"]
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 10
UPDATE_INTERVAL = timedelta(seconds=DEFAULT_UPDATE_INTERVAL)
