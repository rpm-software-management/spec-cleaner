Requires:       zzz-package
%define mydef 1
Name:           preamble-scrambled
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(udev)
Version:        1.0
Release:        0
Summary:        Scrambled preamble
License:        MIT
Source0:        preamble-scrambled.tar.gz
Source0:        preamble-scrambled.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%bcond_with foo
%if %{with foo}
%define incond 1
%endif

%description
Scrambled preamble.

%changelog
