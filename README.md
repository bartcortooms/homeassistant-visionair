# VisionAir Ventilation for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant custom integration for VisionAir (Ventilairsec) ventilation devices via Bluetooth Low Energy.

> **Disclaimer:** This is an unofficial integration not affiliated with Ventilairsec. Use at your own risk.

## Supported Devices

All devices in the Vision'R range that advertise as "VisionAir" over BLE:

| Model | Hardware Max | Status |
|-------|-------------|--------|
| **Purevent Vision'R** | 350 m³/h | ✅ Tested |
| **Urban Vision'R** | 201 m³/h | ⚠️ Untested |
| **Cube Vision'R** | ? | ⚠️ Untested |

## Features

### Fan Entity
- Speed control: Low / Medium / High
- Boost mode preset (30 minutes high airflow)

### Sensors
- Current airflow (m³/h)
- Airflow mode (low/medium/high)
- Remote temperature
- Probe 1 temperature (resistor outlet)
- Probe 2 temperature (air inlet)
- Remote humidity
- Filter life remaining (days)
- Operating days
- Configured volume (m³)

### Switches
- Preheat (winter mode)
- Summer limit

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu → Custom repositories
3. Add `https://github.com/bartcortooms/homeassistant-visionair` as an Integration
4. Search for "VisionAir" and install
5. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/visionair` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Make sure your VisionAir device is powered on
2. Go to Settings → Devices & Services → Add Integration
3. Search for "VisionAir"
4. Select your device from the list of discovered devices

The integration uses Home Assistant's Bluetooth stack, which supports ESPHome Bluetooth proxies automatically.

## Bluetooth Proxy Support

If your Home Assistant device is not within Bluetooth range of your VisionAir device, you can use an [ESPHome Bluetooth Proxy](https://esphome.io/components/bluetooth_proxy.html). Home Assistant will automatically route the connection through the proxy.

## Troubleshooting

### Device not found
- Ensure the device is powered on
- Check that Bluetooth is enabled on your Home Assistant device
- If using a proxy, ensure it's connected and within range of the VisionAir device
- The device can only connect to one client at a time - close the VMI app if it's open

### Connection timeouts
- VisionAir devices may take a few seconds to respond
- Try moving your Bluetooth adapter or proxy closer to the device

## Protocol Documentation

This integration uses the [visionair-ble](https://github.com/bartcortooms/visionair-ble) library. See that repository for detailed protocol documentation.

## License

MIT License - see [LICENSE](LICENSE) for details.
