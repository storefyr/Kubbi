#!/bin/sh
# Samler crash-logs fra VoxeLibre på Sailfish OS og udskriver det vigtigste.
# Kør som normal bruger:  sh collect-crash-logs.sh
# Kopier outputtet og send det i chatten — så gemmer jeg det i repoet.
#
# Fuld rapport gemmes også i /tmp/voxelibre-crash-report.txt

REPORT=/tmp/voxelibre-crash-report.txt
CONF="$HOME/.local/share/luanti/minetest.conf"
: > "$REPORT"

echo "=== VoxeLibre crash report $(date) ===" >> "$REPORT"
echo "" >> "$REPORT"

# 1. Systeminfo
echo "--- System ---" >> "$REPORT"
uname -a >> "$REPORT" 2>&1
free -m | head -n 2 >> "$REPORT"
echo "" >> "$REPORT"

# 2. Seneste debug.txt
echo "--- debug.txt (sidste 40 linjer) ---" >> "$REPORT"
tail -n 40 "$HOME/.minetest/debug.txt" >> "$REPORT" 2>&1
echo "" >> "$REPORT"

# 3. Kør spillet under gdb og fang backtrace
echo "--- gdb backtrace ---" >> "$REPORT"
gdb -batch \
    -ex 'set pagination off' \
    -ex run \
    -ex 'bt 30' \
    -ex 'info threads' \
    -ex 'thread apply all bt 8' \
    --args /usr/bin/luanti --gameid voxelibre --config "$CONF" \
    >> "$REPORT" 2>&1
echo "" >> "$REPORT"

# 4. GPU/driver-relaterede kernel-beskeder (kræver root)
echo "--- dmesg (mali/gpu/drm, sidste 20) ---" >> "$REPORT"
devel-su dmesg 2>/dev/null | grep -iE 'mali|gpu|drm|hang|reset|page.?fault|oom' | tail -n 20 >> "$REPORT"
echo "" >> "$REPORT"

# 5. journalctl for luanti/EGL/Mali (kræver root)
echo "--- journalctl (luanti/egl/mali/oom, sidste 20) ---" >> "$REPORT"
devel-su journalctl -b --no-pager 2>/dev/null | grep -iE 'luanti|mali|egl|killed|segfault|oom|core' | tail -n 20 >> "$REPORT"
echo "" >> "$REPORT"

# 6. Aktuel konfiguration (kun grafik-relevante indstillinger)
echo "--- minetest.conf (grafik-indstillinger) ---" >> "$REPORT"
grep -iE 'video_driver|fullscreen|screen_|vsync|fsaa|antialias|mip_map|shader|post_proc|bloom|volumetric|auto_exposure|mesh_cache|viewing_range|max_block|texture_min|undersampling|client_mapblock|enable_particles|clouds|enable_fog|smooth_light|node_highlight|enable_minimap|translucent|enable_damage|active_block|active_object' "$CONF" >> "$REPORT" 2>&1

# --- Udskriv kun det vigtigste ---
clear
echo "===== VOXELIBRE CRASH ESSENS ====="
echo ""

echo ">>> SYSTEM + RAM"
echo "----------------------------------------"
sed -n '/^--- System ---/,/^--- debug.txt/p' "$REPORT" | grep -v '^--- ' | grep -v '^$'
echo ""

echo ">>> SPILLETS LOG (debug.txt, sidste 12)"
echo "----------------------------------------"
sed -n '/^--- debug.txt/,/^--- gdb/p' "$REPORT" | grep -v '^--- ' | grep -v '^$' | tail -n 12
echo ""

echo ">>> GDB BACKTRACE"
echo "----------------------------------------"
sed -n '/^--- gdb backtrace ---/,/^--- dmesg/p' "$REPORT" \
  | grep -E 'Program received|signal SIG|#[0-9]+|assert|Assertion|COpenGL|Texture|glGen|Thread [0-9]|exited with|Inferior' \
  | head -n 35
echo ""

echo ">>> GPU/KERNEL-FEJL (Mali, dmesg)"
echo "----------------------------------------"
sed -n '/^--- dmesg/,/^--- journalctl/p' "$REPORT" | grep -v '^--- ' | grep -v '^$'
echo ""

echo ">>> JOURNAL (EGL, OOM, kills)"
echo "----------------------------------------"
sed -n '/^--- journalctl/,/^--- minetest/p' "$REPORT" | grep -v '^--- ' | grep -v '^$'
echo ""

echo ">>> GRAFIK-KONFIGURATION"
echo "----------------------------------------"
sed -n '/^--- minetest.conf/,$p' "$REPORT" | grep -v '^--- minetest.conf' | grep -v '^$'
echo ""
echo "===== SLUT PÅ ESSENS ====="
echo "Fuld rapport: $REPORT ($(wc -l < "$REPORT" | tr -d ' ') linjer)"
