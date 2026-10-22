Name:           pkgconfig-already-declared
Version:        1.0
Release:        0
Summary:        pkgconfig insertion stays off when the tool is already declared
License:        MIT
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(474module)
BuildRequires:  pkgconfig(474other) >= 2.0

%description
The BuildRequires already declare pkgconfig, so the cleaner must not
add a second declaration line.

%changelog
