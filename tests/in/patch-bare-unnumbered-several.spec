Name:           patch-bare-unnumbered-several
Version:        1.0
Release:        0
Summary:        Number only the first unnumbered patch for a bare patch macro
License:        MIT
URL:            https://example.com
Patch:          bare.patch
Patch3:         three.patch
Patch:          four.patch

%description
Only the first unnumbered patch is patch 0, the next one keeps number 4.

%prep
%setup -q
%patch -p1
%patch -P 3 -p1
%patch -P 4 -p1

%changelog
