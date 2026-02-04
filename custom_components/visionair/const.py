"""Constants for VisionAir integration."""

DOMAIN = "visionair"

# Configuration
CONF_DEVICE_ADDRESS = "device_address"
CONF_UPDATE_INTERVAL = "update_interval"

# Default update interval in seconds (5 minutes to avoid blocking VMI app connections)
DEFAULT_UPDATE_INTERVAL = 300

# Fan speed modes
SPEED_LOW = "low"
SPEED_MEDIUM = "medium"
SPEED_HIGH = "high"

# Preset modes
PRESET_NONE = "none"
PRESET_BOOST = "boost"
