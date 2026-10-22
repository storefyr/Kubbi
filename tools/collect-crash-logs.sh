#!/bin/sh
# Minimal crash-diagnose for VoxeLibre på Sailfish OS.
# Kør som normal bruger:  sh collect-crash-logs.sh
# Output er KORT — kopier det hele på én gang og send det i chatten.

CONF="$HOME/.local/share/luanti/minetest.conf"
TMPCONF=/tmp/minetest-debug.conf
cp "$CONF" "$TMPCONF" 2>/dev/null || true
echo "opengl_debug = true" >> "$TMPCONF"
export SDL_VIDEODRIVER=wayland

echo "=== DIAGNOSE START $(date '+%H:%M:%S') ==="
echo ""

echo "--- gdb (kører spillet, crasher med vilje) ---"
gdb -batch -ex 'set pagination off' -ex run -ex 'bt 20' \
    --args /usr/bin/luanti --gameid voxelibre --config "$TMPCONF" 2>&1 \
  | grep -E 'Program received|signal SIG|#[0-9]+|Assertion|assert|exited'
echo ""

echo "--- debug.txt (sidste 8 linjer) ---"
tail -n 8 "$HOME/.minetest/debug.txt" 2>&1
echo ""

echo "--- dmesg Mali/GPU ---"
devel-su dmesg 2>/dev/null | grep -iE 'mali|gpu|drm|hang|reset|oom' | tail -n 5
echo ""

echo "--- Grafik-config ---"
grep -iE '^(video_driver|fullscreen|screen_w|screen_h|vsync|fsaa|antialiasing|mip_map|enable_shaders|enable_post_processing|enable_bloom|enable_mesh_cache|viewing_range|max_block_send_distance|max_block_generate_distance|texture_min_size|undersampling|client_mapblock_limit|enable_particles|clouds|enable_fog|smooth_lighting|node_highlighting|enable_minimap|active_block_range|active_object_send_range_blocks|opengl_debug) ' "$CONF" 2>&1
echo ""
echo "=== DIAGNOSE SLUT ==="
