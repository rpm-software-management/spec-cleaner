Name:           patches-unnumbered
Version:        1.0
Release:        0
Summary:        Keep unnumbered patches unnumbered
License:        MIT
URL:            https://example.com
Patch1:         one.patch
Patch2:         two.patch
Patch5:         five.patch
Patch:          six.patch
Patch:          seven.patch

%description
rpm numbers a Patch without number after the highest patch number above it,
so it must stay unnumbered and keep that position when the patches are sorted.

%prep
%autosetup -p1

%changelog
