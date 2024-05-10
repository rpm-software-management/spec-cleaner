#
# spec file for package mingw32-clutter
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%{_mingw32_package_header_debug}
Name:           mingw32-clutter
Version:        1.6.20
Release:        0
Summary:        The clutter library
License:        LGPL-2.1-or-later
# FIXME: use correct group or remove it, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Development/Libraries
URL:            https://clutter-project.org/
Source:         https://www.clutter-project.org/sources/clutter/1.5/clutter-%{version}.tar.bz2
Patch0:         clutter-1.6.14-windows.patch
Patch1:         clutter-1.6.20-ldl.patch
# Native version for glib-genmarshal
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  mingw32-atk-devel
BuildRequires:  mingw32-cairo-devel
BuildRequires:  mingw32-cross-binutils
BuildRequires:  mingw32-cross-gcc
BuildRequires:  mingw32-cross-pkg-config
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gdk-pixbuf-devel
BuildRequires:  mingw32-glib2-devel
BuildRequires:  mingw32-json-glib-devel
BuildRequires:  mingw32-libtool
BuildRequires:  mingw32-pango-devel
BuildRequires:  mingw32-win_iconv-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gmodule-export-2.0)
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(gtk-doc)
#!BuildIgnore:  post-build-checks
Requires:       %{name}-lang = %{version}
BuildArch:      noarch

%description
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces. This package contain the
shared library.

%package -n mingw32-libclutter-win32-1_0-0
Summary:        MinGW Windows port of the Clutter library
Group:          System/Libraries
Obsoletes:      mingw32-clutter
Provides:       mingw32-clutter

%description -n mingw32-libclutter-win32-1_0-0
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces. This package contain the
shared library.

%package devel
Summary:        The clutter library (Development)
# FIXME: use correct group or remove it, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          Development/Libraries
Requires:       mingw32-glee-devel

%description devel
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces. This package contain the
files for development.

%{_mingw32_debug_package}

%lang_package

%prep
%setup -q -n clutter-%{version}

%patch -P 0 -p1 -b .windows
%patch -P 1 -p1 -b .ldl

%build
libtoolize --force --copy --install
autoreconf -f -i
echo "lt_cv_deplibs_check_method='pass_all'" >>%{_mingw32_cache}
PATH="%{_mingw32_bindir}:$PATH" \
%_mingw32_configure \
	--disable-static --enable-shared \
	--with-flavour=win32 \
	--disable-glibtest --disable-conformance
%make_build || make

%install
%make_install

%find_lang clutter-1.0

%files -n mingw32-libclutter-win32-1_0-0
%{_mingw32_bindir}/libclutter-win32-1.0-0.dll

%files lang -f clutter-1.0.lang

%files devel
%{_mingw32_includedir}/clutter-1.0
%{_mingw32_libdir}/libclutter-win32-1.0.dll.a
%{_mingw32_libdir}/pkgconfig/clutter-win32-1.0.pc
%{_mingw32_libdir}/pkgconfig/cally-1.0.pc
%{_mingw32_libdir}/pkgconfig/cogl-gl-1.0.pc
%{_mingw32_libdir}/pkgconfig/cogl-1.0.pc
%{_mingw32_libdir}/pkgconfig/clutter-1.0.pc
%{_mingw32_datadir}/gtk-doc/html/cally
%{_mingw32_datadir}/gtk-doc/html/clutter
%{_mingw32_datadir}/gtk-doc/html/cogl

%changelog
