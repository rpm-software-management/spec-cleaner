Name:           exo
Version:        1.0
Release:        0
Summary:        Keep subpackage Recommends on the lang package
License:        MIT

%description
The lang package supplements only the package it is named after, so a
subpackage that recommends it may be the only one pulling it in.

%package -n libexo-2-0
Summary:        Library
Recommends:     %{name}-lang = %{version}

%description -n libexo-2-0
Library.

%package tools
Summary:        Tools
%if 0%{?suse_version}
Recommends:     %{name}-lang
%endif

%description tools
Tools.

%lang_package -r libexo-2-0

%changelog
