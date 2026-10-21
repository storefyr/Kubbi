%define luanti_version 5.12.0

Name:     luanti
Version:  %{luanti_version}
Release:  1
Summary:  Luanti voxel game engine (client) for Sailfish OS
License:  LGPL-2.1-or-later
URL:      https://www.luanti.org/
# The tag archive contains IrrlichtMt (irr/) and bundled Lua/mini-gmp/jsoncpp
# in lib/, so no submodules are needed. SHA256 of the git-archive tarball
# (identical to the GitHub auto-generated tag tarball):
#   ec853ac6a0020a38da9e9cecf51717d5b86de70a2e073843abeeeca943f9eac9
Source0:  https://github.com/luanti-org/luanti/archive/refs/tags/%{luanti_version}.tar.gz

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
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  sqlite3-devel
BuildRequires:  pkgconfig(sqlite3)
# LuaJIT is strongly preferred on a phone. Not all Sailfish targets ship it;
# Luanti then falls back to its bundled Lua 5.1 interpreter. If it exists it
# will be picked up automatically by cmake/Modules/FindLuaJIT.cmake.
BuildRequires:  lua51-luajit-devel
# Sound (Sailfish ships the "OpenAL" package, see sailfishos/libopenal)
BuildRequires:  OpenAL-devel
BuildRequires:  pkgconfig(openal)
BuildRequires:  libvorbis-devel
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  libogg-devel
BuildRequires:  pkgconfig(ogg)
# GMP/jsoncpp fall back to bundled mini-gmp/jsoncpp if absent.
BuildRequires:  gmp-devel
BuildRequires:  jsoncpp-devel

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

%prep
%autosetup -n luanti-%{luanti_version}

%build
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
    -DENABLE_LUAJIT=ON \
    -DENABLE_LTO=OFF \
    -DENABLE_GLES2=ON \
    -DENABLE_OPENGL=OFF \
    -DENABLE_OPENGL3=OFF \
    -DUSE_SDL2=ON
%cmake_build

%install
%cmake_install
# We ship our own .desktop/launcher for the game package; drop upstream's.
rm -f %{buildroot}%{_datadir}/applications/org.luanti.luanti.desktop
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_mandir}
# Games are installed by game packages, not by the engine.
rm -rf %{buildroot}%{_datadir}/luanti/games

%files
%license LICENSE.txt COPYING.LESSER
%{_bindir}/luanti
%{_datadir}/luanti/
%exclude %{_datadir}/luanti/games

%changelog
* Wed Oct 21 2026 storefyr <storefyr@users.noreply.github.com> - 5.12.0-1
- Initial Sailfish OS package: SDL2/Wayland client with OpenGL ES 2 renderer
