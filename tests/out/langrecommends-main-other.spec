%define _name foo
Name:           gnome-foo
Version:        1.0
Release:        0
Summary:        Keep main package Recommends on another package's lang package
License:        MIT
Recommends:     %{_name}-lang
Recommends:     %{name}-common-lang
Recommends:     libfoo-data-lang
%if 0%{?suse_version}
Recommends:     libfoo-data-lang >= %{version}
%endif

%description
The lang package supplements only the package it is named after, so the
main package drops only the Recommends on its own %%{name}-lang.

%package -n libfoo-data
Summary:        Data

%description -n libfoo-data
Data.

%package -n %{_name}
Summary:        Tool

%description -n %{_name}
Tool.

%package common
Summary:        Common files

%description common
Common files.

%lang_package
%lang_package -n libfoo-data
%lang_package -n %{_name}
%lang_package -n %{name}-common

%changelog
