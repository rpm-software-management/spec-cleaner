Name:           pkgconfig-multiarch-conversions
Version:        1.0
Release:        0
Summary:        Convert only to modules provided on every architecture
License:        MIT
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3-talloc-devel
BuildRequires:  libxml2-devel

%description
The conversion data lists a package once per architecture, so only the
modules every architecture provides are used.

%changelog
