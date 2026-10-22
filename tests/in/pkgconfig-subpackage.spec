Name:           pkgconfig-subpackage
Version:        1.0
Release:        0
Summary:        pkgconfig insertion happens per preamble
License:        MIT
BuildRequires:  pkgconfig(474module)

%description
Main preamble.

%package sub
Summary:        Sub package
BuildRequires:  pkgconfig(474submodule)

%description sub
Sub preamble with its own pkgconfig() dependency and no declaration
of its own, so it gains its own declaration line.

%changelog
