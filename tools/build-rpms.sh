#!/bin/sh
# Build the luanti + harbour-voxelibre RPMs inside the Sailfish Platform SDK.
#
# Usage (inside the Sailfish SDK, e.g. via `sfdk engine exec` or the docker
# image from the Dockerfile in this repository):
#
#   sh tools/build-rpms.sh [SailfishOS-target]
#
# Default target: SailfishOS-5.1.0.11-aarch64 (apps built against 5.1 run on
# Sailfish OS 5.2, e.g. the Jolla Phone (2026)).
set -eu

TARGET="${1:-SailfishOS-5.1.0.11-aarch64}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-$REPO_ROOT/RPMS}"

SB="sb2 -t $TARGET"

# Stage a self-contained source tree for mb2: the spec plus every file it
# references (local Source1-7 for the game package must sit next to the spec).
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/rpm"
cp "$REPO_ROOT/rpm/luanti.spec" "$WORK/rpm/"
cp "$REPO_ROOT/rpm/harbour-voxelibre.spec" "$WORK/rpm/"
cp "$REPO_ROOT/packaging/launch.sh" "$WORK/rpm/"
cp "$REPO_ROOT/packaging/minetest.conf" "$WORK/rpm/"
cp "$REPO_ROOT/packaging/harbour-voxelibre.desktop" "$WORK/rpm/"
cp "$REPO_ROOT/icons/hicolor/86x86/apps/harbour-voxelibre.png"  "$WORK/rpm/harbour-voxelibre-86.png"
cp "$REPO_ROOT/icons/hicolor/108x108/apps/harbour-voxelibre.png" "$WORK/rpm/harbour-voxelibre-108.png"
cp "$REPO_ROOT/icons/hicolor/128x128/apps/harbour-voxelibre.png" "$WORK/rpm/harbour-voxelibre-128.png"
cp "$REPO_ROOT/icons/hicolor/172x172/apps/harbour-voxelibre.png" "$WORK/rpm/harbour-voxelibre-172.png"

# Engine: luanti 5.12.0 (aarch64)
$SB mb2 -t "$TARGET" -s "$WORK/rpm/luanti.spec" -o "$OUT" build

# Game: harbour-voxelibre 0.92.3 (noarch)
$SB mb2 -t "$TARGET" -s "$WORK/rpm/harbour-voxelibre.spec" -o "$OUT" build

echo
echo "RPMs written to $OUT:"
ls -la "$OUT"
