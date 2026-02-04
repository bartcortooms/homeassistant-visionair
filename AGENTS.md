# Instructions for AI Agents

## Library Sync Workflow

The `visionair_ble` library under `custom_components/visionair/visionair_ble/` is a **bundled copy** synced from the standalone library repo at `../visionair-ble`.

**Do not modify the bundled copy directly.** Instead:

1. Make changes in the source repo: `../visionair-ble/src/visionair_ble/`
2. Run the sync script: `./scripts/sync_visionair_ble.sh`
3. Commit changes in both repos as needed

## Testing

Tests are in the library repo (`../visionair-ble/tests/`).

```bash
cd ../visionair-ble
.venv/bin/pytest -v           # Run unit tests
.venv/bin/pytest -m e2e -v    # Run e2e tests (requires real device)
```

E2E tests require an actual VisionAir device and are skipped by default.
