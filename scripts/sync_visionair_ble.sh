#!/bin/bash
# Sync visionair_ble library from the standalone library repo
# Run from the homeassistant-visionair repo root
#
# WORKFLOW:
#   1. Make changes in the visionair-ble repo (src/visionair_ble/)
#   2. Run tests: cd <visionair-ble> && uv run pytest
#   3. Commit changes in visionair-ble
#   4. Run this script: ./scripts/sync_visionair_ble.sh
#   5. Commit changes in homeassistant-visionair
#
# Set LIB_REPO to override the default source path (../visionair-ble).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LIB_REPO="${LIB_REPO:-$REPO_ROOT/../visionair-ble}"
LIB_DIR="$LIB_REPO/src/visionair_ble"
HA_DIR="$REPO_ROOT/custom_components/visionair/visionair_ble"

if [[ ! -d "$LIB_DIR" ]]; then
    echo "Error: Library not found at $LIB_DIR"
    echo "Set LIB_REPO env var to point to visionair-ble repo"
    exit 1
fi

# Check for uncommitted changes in the library repo
LIB_DIRTY=""
if ! (cd "$LIB_REPO" && git diff --quiet && git diff --cached --quiet); then
    LIB_DIRTY="-dirty"
    echo ""
    echo "WARNING: Library repo has uncommitted changes!"
    echo "  Consider committing first: cd $LIB_REPO && git status"
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted. Commit changes in the library repo first."
        exit 1
    fi
fi

LIB_COMMIT=$(cd "$LIB_REPO" && git rev-parse --short HEAD)
LIB_BRANCH=$(cd "$LIB_REPO" && git rev-parse --abbrev-ref HEAD)

echo "Syncing visionair_ble library"
echo "  Source: $LIB_DIR"
echo "  Target: $HA_DIR"
echo "  Commit: $LIB_COMMIT$LIB_DIRTY ($LIB_BRANCH)"

rm -rf "$HA_DIR"
mkdir -p "$HA_DIR"
cp "$LIB_DIR"/*.py "$HA_DIR/"
cp "$LIB_DIR"/py.typed "$HA_DIR/" 2>/dev/null || true

cat > "$HA_DIR/.sync_info" << EOF
# Synced from visionair-ble @ $LIB_COMMIT$LIB_DIRTY ($LIB_BRANCH)
# Date: $(date -Iseconds)
EOF

echo ""
echo "Done! Synced library from $LIB_COMMIT$LIB_DIRTY"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit: git add -A && git commit -m 'Sync library with visionair-ble ($LIB_COMMIT)'"
