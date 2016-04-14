#
# spec file for package rpmpreamble
#
# Copyright (c) 2013 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2010,2011,2012  Stephan Kleine
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


%global libmicrohttpd libmicrohttpd12
Name:           libmicrohttpd
Version:        0.9.49
Release:        0
Summary:        Small Embeddable HTTP Server Library
License:        LGPL-2.1+
Group:          Productivity/Networking/Web/Servers
Url:            https://www.gnu.org/software/libmicrohttpd/
Source0:        http://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
Source1:        http://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz.sig
Source2:        libmicrohttpd.keyring
# PATCH-WORKAROUND-OPENSUSE: the threads have a problem deadlocking (in OBS)
Patch1:         disable-stalling-test.patch
Patch2:         libmicrohttpd_test_data.patch
BuildRequires:  curl
BuildRequires:  file-devel
BuildRequires:  libgcrypt-devel >= 1.2.4
BuildRequires:  libtool
BuildRequires:  makeinfo
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  socat
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libtasn1)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
GNU libmicrohttpd is a small C library that is supposed to make it easy to run
an HTTP server as part of another application. GNU libmicrohttpd is free software
and part of the GNU project. Key features that distinguish libmicrohttpd from
other projects are:

    * C library: fast and small
    * API is simple, expressive and fully reentrant
    * Implementation is http 1.1 compliant
    * HTTP server can listen on multiple ports
    * Support for IPv6
    * Support for incremental processing of POST data
    * Creates binary of only 30k (without TLS/SSL support)
    * Three different threading models
    * Supported platforms include GNU/Linux, FreeBSD, OpenBSD, NetBSD, OS X, W32,
      Symbian and z/OS
    * Optional support for SSL3 and TLS (requires libgcrypt)

libmicrohttpd was started because the author needed an easy way to add a concurrent
HTTP server to other projects. Existing alternatives were either non-free, not
reentrant, standalone, of terrible code quality or a combination thereof. Do not
use libmicrohttpd if you are looking for a standalone http server, there are many
other projects out there that provide that kind of functionality already. However,
if you want to be able to serve simple WWW pages from within your C or C++
application, check it out.

%package -n %{libmicrohttpd}
Summary:        Small embeddable http server library
Group:          System/Libraries

%description -n %{libmicrohttpd}
Shared library for %{name} (%{summary}).

%package devel
Summary:        Small Embeddable HTTP Server Library
Group:          Development/Libraries/C and C++
Requires:       %{libmicrohttpd} = %{version}
Requires:       pkg-config
Requires:       pkgconfig(gnutls)
Requires(post): info
Requires(preun): info

%description devel
Headers, pkg-config files, so link and other development files for %{name}
(%{summary}).

%prep
%setup -q
%patch1
%patch2

%build
%configure \
  --enable-bauth \
  --enable-dauth \
  --enable-epoll \
  --enable-messages \
  --enable-postprocessor \
  --enable-https \
  --disable-static \
  --disable-examples \
  --enable-curl
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
# Paralel execution of tests fail
make -j 1 check

%post -n %{libmicrohttpd} -p /sbin/ldconfig
%postun -n %{libmicrohttpd} -p /sbin/ldconfig
%post devel
%install_info --info-dir=%{_infodir} %{_infodir}/libmicrohttpd.info%{ext_info}
%install_info --info-dir=%{_infodir} %{_infodir}/libmicrohttpd-tutorial.info%{ext_info}

%preun devel
%install_info_delete --info-dir=%{_infodir} %{_infodir}/libmicrohttpd.info%{ext_info}
%install_info_delete --info-dir=%{_infodir} %{_infodir}/libmicrohttpd-tutorial.info%{ext_info}

%files -n %{libmicrohttpd}
%defattr(-,root,root)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog
%{_includedir}/microhttpd.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_infodir}/%{name}*.info%{ext_info}
%{_mandir}/man3/%{name}.3%{ext_man}

%changelog
