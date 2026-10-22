#!/bin/sh
# Samler og viser crash-logs fra VoxeLibre på Sailfish OS.
# Kør som normal bruger (ikke root):  sh collect-crash-logs.sh
# Scriptet kører spillet under gdb, fanger backtrace og viser
# kun de vigtigste sektioner.

OUT=/tmp/voxelibre-crash-report.txt
CONF="$HOME/.local/share/luanti/minetest.conf"
: > "$OUT"

echo "=== VoxeLibre crash report $(date) ===" >> "$OUT"
echo "" >> "$OUT"

# 1. Systeminfo
echo "--- System ---" >> "$OUT"
uname -a >> "$OUT" 2>&1
free -m | head -n 2 >> "$OUT"
echo "" >> "$OUT"

# 2. Seneste debug.txt
echo "--- debug.txt (sidste 40 linjer) ---" >> "$OUT"
tail -n 40 "$HOME/.minetest/debug.txt" >> "$OUT" 2>&1
echo "" >> "$OUT"

# 3. Kør spillet under gdb og fang backtrace
echo "--- gdb backtrace ---" >> "$OUT"
gdb -batch \
    -ex 'set pagination off' \
    -ex run \
    -ex 'bt 30' \
    -ex 'info threads' \
    -ex 'thread apply all bt 8' \
    --args /usr/bin/luanti --gameid voxelibre --config "$CONF" \
    >> "$OUT" 2>&1
echo "" >> "$OUT"

# 4. GPU/driver-relaterede kernel-beskeder (kræver root)
echo "--- dmesg (mali/gpu/drm, sidste 20) ---" >> "$OUT"
devel-su dmesg 2>/dev/null | grep -iE 'mali|gpu|drm|hang|reset|page.?fault|oom' | tail -n 20 >> "$OUT"
echo "" >> "$OUT"

# 5. journalctl for luanti/EGL/Mali (kræver root)
echo "--- journalctl (luanti/egl/mali/oom, sidste 20) ---" >> "$OUT"
devel-su journalctl -b --no-pager 2>/dev/null | grep -iE 'luanti|mali|egl|killed|segfault|oom|core' | tail -n 20 >> "$OUT"
echo "" >> "$OUT"

# 6. Aktuel konfiguration (kun grafik-relevante indstillinger)
echo "--- minetest.conf (grafik-indstillinger) ---" >> "$OUT"
grep -iE 'video_driver|fullscreen|screen_|vsync|fsaa|antialias|mip_map|shader|post_proc|bloom|volumetric|auto_exposure|mesh_cache|viewing_range|max_block|texture_min|undersampling|client_mapblock|enable_particles|clouds|enable_fog|smooth_light|node_highlight|enable_minimap|translucent|enable_damage|active_block|active_object' "$CONF" >> "$OUT" 2>&1
echo "" >> "$OUT"

# --- Udskriv kun de vigtigste sektioner ---
clear
echo "========================================"
echo "  VoxeLibre crash-diagnose"
echo "========================================"
echo ""

echo ">>> 1. SYSTEM + RAM"
echo "----------------------------------------"
sed -n '/^--- System ---/,/^$/p' "$OUT" | grep -v '^--- System ---' | grep -v '^$'
echo ""

echo ">>> 2. SPILLETS EGEN LOG (debug.txt, sidste 15 linjer)"
echo "----------------------------------------"
sed -n '/^--- debug.txt/,/^--- gdb/p' "$OUT" | grep -v '^--- debug.txt' | grep -v '^--- gdb' | grep -v '^$' | tail -n 15
echo ""

echo ">>> 3. GDB BACKTRACE (hvor crashet sker)"
echo "----------------------------------------"
sed -n '/^--- gdb backtrace ---/,/^--- dmesg/p' "$OUT" \
  | grep -E 'Program received|signal SIG|#[0-9]+|assert|Assertion|COpenGL|Texture|glGen|Thread [0-9]|exited' \
  | head -n 40
echo ""

echo ">>> 4. GPU/KERNEL-FEJL (Mali, dmesg)"
echo "----------------------------------------"
sed -n '/^--- dmesg/,/^--- journalctl/p' "$OUT" | grep -v '^--- dmesg' | grep -v '^--- journalctl' | grep -v '^$'
echo ""

echo ">>> 5. JOURNAL (EGL, OOM, kills)"
echo "----------------------------------------"
sed -n '/^--- journalctl/,/^--- minetest/p' "$OUT" | grep -v '^--- journalctl' | grep -v '^--- minetest' | grep -v '^$'
echo ""

echo ">>> 6. AKTUEL GRAFIK-KONFIGURATION"
echo "----------------------------------------"
sed -n '/^--- minetest.conf/,$p' "$OUT" | grep -v '^--- minetest.conf' | grep -v '^$'
echo ""

echo "========================================"
echo "  Fuld rapport gemt i: $OUT"
echo "========================================"
