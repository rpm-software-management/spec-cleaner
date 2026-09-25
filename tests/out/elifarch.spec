Name:           elifarch
Version:        1.0
Release:        0
Summary:        Test %%elifarch and %%elifos branches in the preamble
License:        MIT
URL:            https://example.org/
%ifarch x86_64
BuildRequires:  pkgconfig(x86lib)
%elifarch aarch64
BuildRequires:  pkgconfig(armlib)
%else
BuildRequires:  pkgconfig(genericlib)
%endif
%ifos linux
Requires:       linux-helper
%elifos freebsd
Requires:       bsd-helper
%endif

%description
Test.

%changelog
