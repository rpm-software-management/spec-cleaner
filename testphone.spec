#
# spec file for package sflphone
#
# Copyright (c) 2013-2014  Ákos Szőts <szotsaki@gmail.com>
# Copyright (c) 2009-2010  Vovochka404 <vovochka13@gmail.com>
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

%bcond_without common
%bcond_without kde4
%bcond_without plugins
%bcond_without gnome

Name:           sflphone
Version:        1.3.0.git
Release:        0
Summary:        Open source SIP/IAX2 compatible enterprise-class softphone
License:        GPL-3.0
Group:          Productivity/Telephony/SIP/Clients
Url:            http://sflphone.org/
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}-kde-%{version}.tar.xz
BuildRequires:  autoconf
BuildRequires:  fdupes
BuildRequires:  find
BuildRequires:  libtool
BuildRequires:  sed
BuildRequires:  update-desktop-files
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if %{with common}
BuildRequires:  ilbc
BuildRequires:  libasound2
BuildRequires:  libgsm-devel
BuildRequires:  libyaml-devel
BuildRequires:  patch
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(celt)
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  pkgconfig(cryptopp)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-c++-1)
BuildRequires:  pkgconfig(dbus-c++-glib-1)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libccext2)
BuildRequires:  pkgconfig(libccgnu2)
BuildRequires:  pkgconfig(libccrtp)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libpcre16)
BuildRequires:  pkgconfig(libpcrecpp)
BuildRequires:  pkgconfig(libpcreposix)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libsystemd-daemon)
BuildRequires:  pkgconfig(libsystemd-id128)
BuildRequires:  pkgconfig(libsystemd-journal)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(libzrtpcpp)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(rarian)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(uuid)
Suggests:       %{name}-client-gnome
Suggests:       %{name}-client-kde4
%endif

%if %{with kde4}
# For KDE 4.12
BuildRequires:  akonadi-runtime
BuildRequires:  cmake
BuildRequires:  libkde4-devel
BuildRequires:  libkdepimlibs4-devel
%endif

%if %{with gnome}
BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  yelp-tools
BuildRequires:  pkgconfig(clutter-gtk-1.0)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(gnome-doc-utils)
BuildRequires:  pkgconfig(libnotify)
%endif

%if %{with plugins}
%if 0%{?suse_version} >= 1310
BuildRequires:  pkgconfig(camel-1.2)
BuildRequires:  pkgconfig(evolution-data-server-1.2)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(libebackend-1.2)
BuildRequires:  pkgconfig(libebook-1.2)
BuildRequires:  pkgconfig(libebook-contacts-1.2)
BuildRequires:  pkgconfig(libecal-1.2)
BuildRequires:  pkgconfig(libedata-book-1.2)
BuildRequires:  pkgconfig(libedata-cal-1.2)
BuildRequires:  pkgconfig(libedataserver-1.2)
%else
BuildRequires:  evolution-data-server-devel
%endif # 0% {?suse_version}
%endif

%description
SFLphone is an open-source SIP/IAX2 compatible enterprise-class softphone

%if %{with kde4}

%package -n %{name}-client-kde4
Summary:        KDE 4 Backend for sflphone
Group:          Productivity/Telephony/SIP/Clients
Requires:       %{name} = %{version}-%{release}
# For building with KDE 4.12
# % kde4_akonadi_requires == "Requires: akonadi-runtime  >= 1.10.2 akonadi-runtime < 1.10.40" (on openSUSE 13.1)
Requires:       akonadi-runtime >= %( echo `rpm -q --queryformat '%{VERSION}' akonadi-runtime`)
# % {requies_eq}     akonadi_runtime
%{kde4_runtime_requires}
%{kde4_pimlibs_requires}

%description -n %{name}-client-kde4
KDE 4 backend for SFLphone.
%endif

%if %{with gnome}

%package -n %{name}-client-gnome
Summary:        Gnome Backend for sflphone
Group:          Productivity/Telephony/SIP/Clients
Requires:       %{name} = %{version}-%{release}
Recommends:     %{name}-plugins
%{?glib2_gsettings_schema_requires: %{glib2_gsettings_schema_requires}}

%description -n %{name}-client-gnome
Gnome backend for SFLphone.
%endif

%if %{with plugins}

%package -n %{name}-plugins
Summary:        Plugins for sflphone (Evolution address book integration)
Group:          Productivity/Telephony/SIP/Clients
Requires:       %{name} = %{version}-%{release}

%description -n %{name}-plugins
Plugins for SFLphone. Currently: Evolution address book integration.
%endif

%prep
%setup -q

# We unpack the -kde variant (-a 1) and move the whole directory from the tarball one level up.
%setup -q -T -c -n %{name}-%{version}/kde/ -a 1

# In the non-git version it's: mv sflphone-client-kde*/* .
mv sflphone-kde*/* .

# Change back to the original directory from kde/
%setup -q -T -D

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%if %{with common}
pushd daemon
pushd libs
./compile_pjsip.sh
popd
./autogen.sh
%configure --with-libilbc --with-opus --enable-ipv6 --disable-video
%{make_jobs}
popd
%endif

%if %{with plugins}
pushd plugins
./autogen.sh
%configure
%{make_jobs}
popd
%endif

%if %{with kde4}
pushd kde
# We don't have libavcodec, libswscale etc. by default, so it's disabled
%cmake_kde4 -d build -- -DENABLE_VIDEO=false
%{make_jobs}
popd
%endif

%if %{with gnome}
pushd gnome
./autogen.sh
%configure --disable-video
%{make_jobs}
%endif

%install
%if %{with common}
pushd daemon
%{makeinstall} INSTALL_ROOT=%{buildroot}
popd
%endif

%if %{with plugins}
pushd plugins
%{makeinstall} INSTALL_ROOT=%{buildroot}
popd
%endif

%if %{with kde4}
pushd kde/build/
%{makeinstall} INSTALL_ROOT=%{buildroot}
rm -rf %{buildroot}/%{_includedir}
rm -f %{buildroot}/%{_libdir}/*.so
popd
%suse_update_desktop_file -r %{name}-client-kde Network Telephony
%{kde_post_install}

# In GIT version it's unnecessary
# % find_lang % {name}-kde % {name}-kde.lang --without-gnome
# % find_lang % {name}-client-kde % {name}-kde.lang --without-gnome --without-kde
%endif

%if %{with gnome}
pushd gnome
%{makeinstall} INSTALL_ROOT=%{buildroot}
popd
%suse_update_desktop_file -r %{name} Network Telephony
%find_lang %{name} %{name}-gnome.lang --without-gnome --without-kde
%endif

%fdupes %{buildroot}

%if %{with common}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/codecs/
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ringtones
%doc %{_mandir}/man1/sflphoned.1.gz
%{_libdir}/%{name}/codecs/*
%{_libdir}/%{name}/sflphoned
%{_datadir}/%{name}/ringtones/*
%{_datadir}/dbus-1/services/*
%endif

%if %{with plugins}

%post -n %{name}-plugins -p /sbin/ldconfig

%postun -n %{name}-plugins -p /sbin/ldconfig

%files -n %{name}-plugins
%defattr(-,root,root)
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/*
%endif

%if %{with kde4}

%post -n %{name}-client-kde4
/sbin/ldconfig
%desktop_database_post

%postun -n %{name}-client-kde4
/sbin/ldconfig
%desktop_database_postun

# GIT: unnecessary:  -f % {name}-kde.lang
%files -n %{name}-client-kde4
%defattr(-,root,root)
%dir %{_kde4_appsdir}/%{name}-client-kde/
%dir %{_kde4_htmldir}/*/%{name}-client-kde/
%doc %{_mandir}/man1/%{name}-client-kde.1.gz
%doc %{_kde4_htmldir}/*/%{name}-client-kde/*
%{_bindir}/%{name}-client-kde
%{_libdir}/*.so.*
%{_kde4_applicationsdir}/%{name}-client-kde.desktop
%{_kde4_appsdir}/%{name}-client-kde/**
%{_kde4_configkcfgdir}/*
%{_datadir}/icons/hicolor/*/apps/%{name}-client-kde.*
%endif

%if %{with gnome}

%post -n %{name}-client-gnome
/sbin/ldconfig
%{glib2_gsettings_schema_post}
%desktop_database_post

%postun -n %{name}-client-gnome
/sbin/ldconfig
%{glib2_gsettings_schema_postun}
%desktop_database_postun

%files -n %{name}-client-gnome -f %{name}-gnome.lang
%defattr(-,root,root)
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/ui/
%doc %{_mandir}/man1/%{name}.1.gz
%doc %{_mandir}/man1/%{name}-client-gnome.1.gz
%{_bindir}/%{name}
%{_bindir}/%{name}-client-gnome
%{_datadir}/%{name}/*.*
%{_datadir}/%{name}/ui/*
%{_datadir}/pixmaps/*
%{_datadir}/glib-2.0/schemas/org.sflphone.SFLphone.gschema.xml
%{_datadir}/applications/%{name}.desktop
%endif

%changelog
