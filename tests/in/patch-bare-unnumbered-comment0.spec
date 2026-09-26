# an unnumbered Patch applied by a bare %patch must be renumbered to Patch0
Name:           patch-bare-unnumbered-comment0
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/patch-bare-unnumbered-comment0
Source0:        foo-%{version}.tar.gz
#Patch0:        commented-out.patch
Patch:          unnumbered.patch

%description
Test package.

%prep
%setup -q
%patch

%build

%files

%changelog
