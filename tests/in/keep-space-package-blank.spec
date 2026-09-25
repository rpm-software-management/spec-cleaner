Name:           keep-space-package-blank
Version:        1.0
Release:        0
Summary:        Blank lines inside a subpackage preamble
License:        MIT

%description
Blank lines inside a subpackage preamble with --keep-space.

%package devel
Summary:        Development files
Group:          Development/Libraries/C and C++

Requires:       %{name} = %{version}
Requires:       bar

# needed for the headers
Requires:       zlib-devel

%description devel
Development files.

%package tools
Summary:        Tools

%if 0%{?suse_version}
Requires:       zzz
%endif
Requires:       aaa

%description tools
Tools.

%files

%files devel

%files tools

%changelog
