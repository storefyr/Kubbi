%define luanti_version 5.12.0
%global debug_package %{nil}

Name:     luanti
Version:  %{luanti_version}
Release:  1
Summary:  Luanti voxel game engine (client) for Sailfish OS
License:  LGPL-2.1-or-later
URL:      https://www.luanti.org/
# The GitHub tag archive contains IrrlichtMt (irr/) and bundled
# Lua/mini-gmp/jsoncpp in lib/, so no submodules are needed.
# SHA256 of the tarball:
#   ec853ac6a0020a38da9e9cecf51717d5b86de70a2e073843abeeeca943f9eac9
Source0:  https://github.com/luanti-org/luanti/archive/refs/tags/%{luanti_version}.tar.gz
# Replace fatal assert(name != 0) in IrrlichtMt's texture cache with a
# graceful skip. On Sailfish OS (Mali-G610 via libhybris) glGenTextures
# can return 0 under GPU memory pressure when loading heavy texture
# atlases (e.g. VoxeLibre's 2874 textures). The assert caused SIGABRT.
Patch0:   luanti-sailfish-gpu-oom.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
# SDL2 + Wayland/GLES stack (Sailfish SDL2 is built Wayland-only)
BuildRequires:  SDL2-devel
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  mesa-llvmpipe-libGLESv1-devel
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libpulse-simple)
# Engine libraries
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libpng)
# Sailfish ships libjpeg-turbo 1.2.1 whose devel package has no .pc file;
# IrrlichtMt's find_package(JPEG) only needs the headers and library.
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libcurl)
# Sailfish's SQLite devel package is named sqlite-devel (ships sqlite3.pc).
BuildRequires:  sqlite-devel
# Sound (Sailfish ships the "OpenAL" package, see sailfishos/libopenal)
BuildRequires:  OpenAL-devel
BuildRequires:  pkgconfig(openal)
BuildRequires:  libvorbis-devel
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  libogg-devel
BuildRequires:  pkgconfig(ogg)
# GMP is available on Sailfish. LuaJIT and jsoncpp are not; Luanti falls
# back to its bundled Lua 5.1 interpreter and bundled jsoncpp.
BuildRequires:  gmp-devel

%description
Luanti (formerly Minetest) is an open source voxel game engine. This package
contains the client, built for Sailfish OS with the SDL2/Wayland backend and
the OpenGL ES 2 renderer. Games (such as VoxeLibre) are packaged separately
and installed into /usr/share/luanti/games.

# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%if 0%{?_chum}
Title: Luanti
Type: desktop-application
PackagedBy: storefyr
Categories:
  - Game
Custom:
  - Repo: https://github.com/luanti-org/luanti
PackageIcon: https://raw.githubusercontent.com/storefyr/Kubbi/refs/heads/main/icons/hicolor/128x128/apps/harbour-voxelibre.png
Links:
  Homepage: https://www.luanti.org/
  Help: https://docs.luanti.org/
  Bugtracker: https://github.com/luanti-org/luanti/issues
%endif

%build
# No %prep section: mb2 runs rpmbuild --noprep and its rpmspec --query
# fails with "second %prep" when meego-rpm-config also injects one.
# Since %prep never runs anyway, we apply the patch manually here.
PATCH_FILE="$PWD/rpm/luanti-sailfish-gpu-oom.patch"
cd luanti-%{luanti_version}
patch -p1 --forward < "$PATCH_FILE" || true
# GLES2-only: Sailfish (Wayland/libhybris) has no desktop GL. IrrlichtMt
# selects the SDL2 device automatically (USE_SDL2=ON) and therefore needs
# no X11. The runtime driver is chosen with "video_driver = ogles2" in
# minetest.conf.
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_CLIENT=ON \
    -DBUILD_SERVER=OFF \
    -DBUILD_UNITTESTS=OFF \
    -DBUILD_BENCHMARKS=OFF \
    -DINSTALL_DEVTEST=OFF \
    -DENABLE_CURL=ON \
    -DENABLE_GETTEXT=OFF \
    -DENABLE_SOUND=ON \
    -DENABLE_CURSES=OFF \
    -DENABLE_LEVELDB=OFF \
    -DENABLE_POSTGRESQL=OFF \
    -DENABLE_REDIS=OFF \
    -DENABLE_SPATIAL=OFF \
    -DENABLE_PROMETHEUS=OFF \
    -DENABLE_LUAJIT=OFF \
    -DENABLE_LTO=OFF \
    -DENABLE_GLES2=ON \
    -DENABLE_OPENGL=OFF \
    -DENABLE_OPENGL3=OFF \
    -DUSE_SDL2=ON
%cmake_build

%install
cd luanti-%{luanti_version}
%cmake_install
# We ship our own .desktop/launcher for the game package; drop upstream's
# desktop file, icons, metainfo, docs, man pages, and the legacy minetest
# symlink.
rm -f %{buildroot}%{_datadir}/applications/org.luanti.luanti.desktop
rm -f %{buildroot}%{_bindir}/minetest
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/icons
rm -rf %{buildroot}%{_datadir}/metainfo
# Games are installed by game packages, not by the engine.
rm -rf %{buildroot}%{_datadir}/luanti/games

%files
%license luanti-%{luanti_version}/LICENSE.txt luanti-%{luanti_version}/COPYING.LESSER
%{_bindir}/luanti
%{_datadir}/luanti/

%changelog
* Wed Oct 21 2026 storefyr <storefyr@users.noreply.github.com> - 5.12.0-1
- Initial Sailfish OS package: SDL2/Wayland client with OpenGL ES 2 renderer
