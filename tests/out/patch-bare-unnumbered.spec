Name:           patch-bare-unnumbered
Version:        1.0
Release:        0
Summary:        Number the unnumbered patch a bare patch macro applies
License:        MIT
URL:            https://example.com
Patch0:         bare.patch
Patch1:         one.patch

%description
The bare patch macro becomes '-P 0', so the unnumbered patch it applied
must become Patch0.

%prep
%setup -q
%patch -P 1 -p1
%patch -P 0 -p1

%changelog
