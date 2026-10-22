#!/bin/sh
# Launcher for VoxeLibre on Sailfish OS. Started from the launcher icon via
# /bin/sh (sailjail refuses to sandbox a shell script directly, so the
# desktop file uses X-Nemo-Application-Type=no-invoker + Sandboxing=Disabled).
#
# Everything user-specific (config, worlds, mods) lives in
# ~/.local/share/luanti (MINETEST_USER_PATH). The game itself is read-only
# under /usr/share/luanti/games/voxelibre.

set -u

USER_PATH="${MINETEST_USER_PATH:-$HOME/.local/share/luanti}"
CONF="$USER_PATH/minetest.conf"
DEFAULT_CONF=/usr/share/harbour-voxelibre/minetest.conf

# Luanti reads MINETEST_USER_PATH to decide where worlds/configs live.
# Without this export, data silently lands in ~/.minetest instead.
export MINETEST_USER_PATH="$USER_PATH"

# Luanti's IrrlichtMt touch layer handles gestures itself; SDL must not also
# synthesise mouse events from the same fingers.
export SDL_TOUCH_MOUSE_EVENTS=0
export SDL_MOUSE_TOUCH_EVENTS=0
# Sailfish SDL2 is built Wayland-only; make it explicit.
export SDL_VIDEODRIVER=wayland

mkdir -p "$USER_PATH"

# First start: seed a phone-friendly config if none exists yet.
if [ ! -f "$CONF" ] && [ -f "$DEFAULT_CONF" ]; then
    cp "$DEFAULT_CONF" "$CONF"
fi

cd "$USER_PATH" || exit 1

exec /usr/bin/luanti \
    --gameid voxelibre \
    --config "$CONF" \
    "$@"
