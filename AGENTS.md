# Instructions for AI Agents

## Library Sync Workflow

The `visionair_ble` library under `custom_components/visionair/visionair_ble/` is a **bundled copy** synced from the standalone [visionair-ble](https://github.com/bartcortooms/visionair-ble) repo.

**Do not modify the bundled copy directly.** Instead:

1. Make changes in the source repo (`visionair-ble/src/visionair_ble/`)
2. Run the sync script: `./scripts/sync_visionair_ble.sh`
3. Commit changes in both repos as needed

The sync script defaults to `../visionair-ble` but this can be overridden with `LIB_REPO`.

## Deploying to Home Assistant

After syncing and pushing, update the integration on the Home Assistant instance via HACS.

The integration is installed via [HACS](https://hacs.xyz/) and can be updated from the CLI using the `hass-cli` WebSocket API:

```bash
# 1. Find the HACS repository ID (one-time lookup)
hass-cli raw ws hacs/repositories/list --json '{}'
# Look for full_name: bartcortooms/homeassistant-visionair → note the id

# 2. Download the update
hass-cli raw ws hacs/repository/download --json '{"repository": "<HACS_REPO_ID>"}'

# 3. Restart Home Assistant to load the new code
hass-cli service call homeassistant.restart
```

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

Tests are in the [visionair-ble](https://github.com/bartcortooms/visionair-ble) repo.

```bash
uv run pytest -v           # Run unit tests
uv run pytest -m e2e -v    # Run e2e tests (requires real device)
```

E2E tests require an actual VisionAir device and are skipped by default.

## Code Style

- **Write for newcomers, not historians.** Code comments and documentation describe **what things are now**, not what they used to be or how they changed. Never use phrases like "formerly", "was previously", "NOT X (see Y)", "changed from", or "used to be" in code or docs. A newcomer reading the code should understand everything without needing to know the project's history.
