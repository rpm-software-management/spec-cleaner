%define pkg_version 2026
Name:           sourceorder-subpackages
Version:        %{pkg_version}
Release:        0
Summary:        Subpackage stanzas keep their written order in minimal mode
License:        Apache-2.0 AND LPPL-1.0
URL:            https://example.org/

%description
Main description written before the subpackage blocks.

%package alpha-bin
Version:        %{pkg_version}.1
Release:        0
License:        LPPL-1.0
Summary:        Binary files of alpha
Group:          Productivity/Publishing/TeX/Utilities
URL:            https://example.org/
Requires(pre):  sourceorder-subpackages-alpha >= %pkg_version
#!BuildIgnore:  sourceorder-subpackages-alpha

%description alpha-bin
Binary files of alpha

%package beta-bin
Version:        %{pkg_version}.2
Release:        0
License:        LPPL-1.0
Summary:        Binary files of beta
Group:          Productivity/Publishing/TeX/Utilities
URL:            https://example.org/
Requires(pre):  sourceorder-subpackages-beta >= %pkg_version
#!BuildIgnore:  sourceorder-subpackages-beta

%description beta-bin
Binary files of beta

%files alpha-bin
%{_bindir}/alpha

%files beta-bin
%{_bindir}/beta
%{_bindir}/beta-helper

%post alpha-bin
/sbin/ldconfig

%post beta-bin
/sbin/ldconfig

%changelog
