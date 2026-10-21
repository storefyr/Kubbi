# Kubbi — VoxeLibre on Sailfish OS

Packages the [VoxeLibre](https://codeberg.org/VoxeLibre/VoxeLibre) survival
sandbox game (a [Luanti](https://www.luanti.org/) game) for Sailfish OS,
targeted at the **Jolla Phone (2026)** (aarch64, Sailfish OS 5.2).

VoxeLibre is not a standalone game — it is game *data* that runs on the Luanti
engine. This repository therefore produces two RPMs:

| Package | Contents |
|---|---|
| `luanti` | Luanti 5.12.0 client engine, built with the SDL2/Wayland backend and the OpenGL ES 2 renderer (`/usr/bin/luanti`, `/usr/share/luanti`) |
| `harbour-voxelibre` | VoxeLibre 0.92.3 game data in `/usr/share/luanti/games/voxelibre`, plus a launcher icon, desktop file and a phone-friendly default config |

## Installing on the phone

1. Enable "allow untrusted software" in **Settings → System → Security**
   (or install [Storeman](https://openrepos.net/content/feeruvang/storeman)).
2. Copy both RPMs to the phone and install them (order matters: engine first):

   ```sh
   devel-su pkcon install-local luanti-5.12.0-1.aarch64.rpm
   devel-su pkcon install-local harbour-voxelibre-0.92.3-1.noarch.rpm
   ```

   Or from the CI artifacts / a release: download both `.rpm` files and install
   them the same way.
3. Start **VoxeLibre** from the app grid. On first start the launcher creates
   `~/.local/share/luanti/minetest.conf` with GLES2/fullscreen/touch defaults.
   Worlds, screenshots and settings live in `~/.local/share/luanti/`.

## Building

The engine is a C++ CMake project and must be cross-compiled with the Sailfish
SDK for `aarch64`. Two options:

### GitHub Actions (easiest)

Push to `main` (or open a PR) — the workflow in
`.github/workflows/build-rpm.yml` builds both RPMs against the
`SailfishOS-5.1.0.11-aarch64` target using the Platform SDK in Docker, and
uploads them as artifacts. (Apps built against the 5.1 target run on
Sailfish OS 5.2.)

### Locally with the Sailfish SDK

```sh
# one-time: install the Sailfish SDK and the aarch64 target
sfdk tooling install SailfishOS-5.1.0.11-aarch64
sfdk target install SailfishOS-5.1.0.11-aarch64

# then, from the repo root:
sfdk engine exec sh tools/build-rpms.sh
```

RPMs are written to `./RPMS/`.

### Locally with Docker

```sh
docker build -t kubbi-sailfish-sdk .
docker run --rm -v "$PWD":/home/mersdk/kubbi -w /home/mersdk/kubbi \
    kubbi-sailfish-sdk sh tools/build-rpms.sh
```

## How it fits together

- `rpm/luanti.spec` — engine. Builds with `-DENABLE_GLES2=ON
  -DENABLE_OPENGL=OFF -DENABLE_OPENGL3=OFF -DUSE_SDL2=ON` because Sailfish
  (Wayland + libhybris) only provides OpenGL ES. LuaJIT is used when present;
  Luanti otherwise falls back to its bundled Lua 5.1, mini-gmp and jsoncpp.
- `rpm/harbour-voxelibre.spec` — game data (noarch). Installs the VoxeLibre
  tree into the engine's games directory.
- `packaging/launch.sh` — launcher run from the icon. Seeds a default
  `minetest.conf` (GLES2, fullscreen, touch controls, conservative view
  distance) on first start, then runs
  `luanti --gameid voxelibre --config ~/.local/share/luanti/minetest.conf`.
- `packaging/harbour-voxelibre.desktop` — uses
  `X-Nemo-Application-Type=no-invoker` and `[X-Sailjail] Sandboxing=Disabled`,
  the proven pattern for fullscreen SDL2 games on Sailfish (sailjail cannot
  sandbox a shell-script `Exec`).
- `packaging/minetest.conf` — the first-start default config.
- `icons/hicolor/*/apps/harbour-voxelibre.png` — launcher icons derived from
  VoxeLibre's `menu/icon.png`.

## Known limitations / TODO

- **Orientation**: the Jolla Phone (2026) is a portrait device and the Wayland
  compositor hands out a portrait surface. Luanti currently renders in the
  native orientation; landscape/rotation handling (as done by e.g.
  `smatkovi/0ad-sailfish` with a self-rotation patch) is not implemented yet.
- **Touch controls** are enabled via `touch_controls = true`; in-game
  playability on the phone still needs on-device testing.
- **Performance**: defaults are conservative (view distance 60). Tweak
  `~/.local/share/luanti/minetest.conf` to taste.
- The build has not yet been verified on-device; CI builds the RPMs, but the
  first real test is on the phone.

## Distribution

The specs are Chum-ready (metadata block in `%description`, spec in `rpm/`,
see [sailfishos-chum/main](https://github.com/sailfishos-chum/main)). To
submit, add an `rpm/_service` file with a `tar_git` service pointing at this
repository and create the package on <https://build.sailfishos.org/>.

## License

Packaging: [GPL-3.0](LICENSE). Luanti: LGPL-2.1-or-later. VoxeLibre: GPL-3.0-or-later
(media under CC-BY-SA-4.0, see the game's `LEGAL.md`).
