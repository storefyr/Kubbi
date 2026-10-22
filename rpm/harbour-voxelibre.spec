%define voxelibre_version 0.92.3

Name:     harbour-voxelibre
Version:  %{voxelibre_version}
Release:  1
Summary:  VoxeLibre - survival sandbox voxel game for Sailfish OS
License:  GPL-3.0-or-later
URL:      https://codeberg.org/VoxeLibre/VoxeLibre
# SHA256 of the GitHub tag tarball:
#   c34858a18b64e03e57ef618a8e113133c5d64c0af3f7ede3d856ee7c04732b23
Source0:  https://github.com/VoxeLibre/VoxeLibre/archive/refs/tags/%{voxelibre_version}.tar.gz
Source1:  launch.sh
Source2:  minetest.conf
Source3:  harbour-voxelibre.desktop
Source4:  harbour-voxelibre-86.png
Source5:  harbour-voxelibre-108.png
Source6:  harbour-voxelibre-128.png
Source7:  harbour-voxelibre-172.png

BuildArch:  noarch

BuildRequires:  desktop-file-utils

Requires:  luanti >= 5.10
Requires:  SDL2

%description
VoxeLibre (formerly Voxelgarden) is a survival sandbox game built on the
Luanti engine: survive, gather, hunt, build and explore a procedurally
generated voxel world.

This package installs the game data into /usr/share/luanti/games/voxelibre
and a launcher icon. It requires the luanti engine package. On first start
the launcher creates a phone-friendly configuration (GLES2 renderer,
fullscreen, touch controls) in ~/.local/share/luanti/minetest.conf.

# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%if 0%{?_chum}
Title: VoxeLibre
Type: desktop-application
PackagedBy: storefyr
Categories:
  - Game
Custom:
  - Repo: https://codeberg.org/VoxeLibre/VoxeLibre
PackageIcon: https://raw.githubusercontent.com/storefyr/Kubbi/refs/heads/main/icons/hicolor/128x128/apps/harbour-voxelibre.png
Screenshots:
  - https://raw.githubusercontent.com/VoxeLibre/VoxeLibre/0.92.3/screenshot.png
Links:
  Homepage: https://voxelibre.github.io/
  Help: https://codeberg.org/VoxeLibre/VoxeLibre
  Bugtracker: https://codeberg.org/VoxeLibre/VoxeLibre/issues
%endif

%prep
%autosetup -n VoxeLibre-%{voxelibre_version}

%build
# Game data only; nothing to compile.

%install
cd VoxeLibre-%{voxelibre_version}

# Game data into the engine's system games directory.
install -d %{buildroot}%{_datadir}/luanti/games/voxelibre
cp -a mods textures menu game.conf settingtypes.txt minetest.conf \
    LICENSE.txt \
    %{buildroot}%{_datadir}/luanti/games/voxelibre/

# Launcher assets.
install -d %{buildroot}%{_datadir}/harbour-voxelibre
install -m 0755 %{SOURCE1} %{buildroot}%{_datadir}/harbour-voxelibre/launch.sh
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/harbour-voxelibre/minetest.conf

# Desktop file (sailjail cannot sandbox a shell script, hence the /bin/sh
# Exec trick and Sandboxing=Disabled).
install -d %{buildroot}%{_datadir}/applications
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/harbour-voxelibre.desktop
desktop-file-install --delete-original \
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/harbour-voxelibre.desktop

# Launcher icons.
install -d %{buildroot}%{_datadir}/icons/hicolor/86x86/apps
install -d %{buildroot}%{_datadir}/icons/hicolor/108x108/apps
install -d %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -d %{buildroot}%{_datadir}/icons/hicolor/172x172/apps
install -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/86x86/apps/harbour-voxelibre.png
install -m 0644 %{SOURCE5} %{buildroot}%{_datadir}/icons/hicolor/108x108/apps/harbour-voxelibre.png
install -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/harbour-voxelibre.png
install -m 0644 %{SOURCE7} %{buildroot}%{_datadir}/icons/hicolor/172x172/apps/harbour-voxelibre.png

%files
%license VoxeLibre-%{voxelibre_version}/LICENSE.txt
%{_datadir}/luanti/games/voxelibre/
%{_datadir}/harbour-voxelibre/
%{_datadir}/applications/harbour-voxelibre.desktop
%{_datadir}/icons/hicolor/86x86/apps/harbour-voxelibre.png
%{_datadir}/icons/hicolor/108x108/apps/harbour-voxelibre.png
%{_datadir}/icons/hicolor/128x128/apps/harbour-voxelibre.png
%{_datadir}/icons/hicolor/172x172/apps/harbour-voxelibre.png

%changelog
* Wed Oct 21 2026 storefyr <storefyr@users.noreply.github.com> - 0.92.3-1
- Initial Sailfish OS package of VoxeLibre 0.92.3
