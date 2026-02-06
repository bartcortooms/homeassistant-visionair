# Instructions for AI Agents

## Library Sync Workflow

The `visionair_ble` library under `custom_components/visionair/visionair_ble/` is a **bundled copy** synced from the standalone library repo at `../visionair-ble`.

**Do not modify the bundled copy directly.** Instead:

1. Make changes in the source repo: `../visionair-ble/src/visionair_ble/`
2. Run the sync script: `./scripts/sync_visionair_ble.sh`
3. Commit changes in both repos as needed

## Deploying to Home Assistant

After syncing and pushing, update the integration on the Home Assistant instance via HACS.

The integration is installed via [HACS](https://hacs.xyz/) and can be updated from the CLI using the `hass-cli` WebSocket API (or the wrapper at `../homeassistant-cli/ha`):

```bash
# 1. Find the HACS repository ID (one-time lookup)
hass-cli raw ws hacs/repositories/list --json '{}'
# Look for full_name: bartcortooms/homeassistant-visionair → note the id

# 2. Download the update
hass-cli raw ws hacs/repository/download --json '{"repository": "<HACS_REPO_ID>"}'

# 3. Restart Home Assistant to load the new code
hass-cli service call homeassistant.restart
```

Or use the wrapper shortcut: `../homeassistant-cli/ha hacs-update`

**Enable/disable the integration** (useful during BLE testing to avoid connection conflicts):

```bash
# Find the config entry ID
hass-cli raw get /api/config/config_entries/entry  # look for domain: visionair

# Disable
hass-cli raw ws config_entries/disable --json '{"entry_id": "<ENTRY_ID>", "disabled_by": "user"}'

# Enable
hass-cli raw ws config_entries/disable --json '{"entry_id": "<ENTRY_ID>", "disabled_by": null}'
```

## Testing

Tests are in the library repo (`../visionair-ble/tests/`).

```bash
cd ../visionair-ble
uv run pytest -v           # Run unit tests
uv run pytest -m e2e -v    # Run e2e tests (requires real device)
```

E2E tests require an actual VisionAir device and are skipped by default.
